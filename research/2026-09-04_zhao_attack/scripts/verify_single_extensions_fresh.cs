// Independent certificate checker. No producer or previous verifier is imported.
// Every leaf's shortest sums come from all 4*3^6 bounded coefficient tuples.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text.Json;

public static class SingleExtensionsFreshAudit
{
    const int Q = 625, Infinite = 99, Cutoff = 13;
    static readonly int[] Basis = { 1, 5, 25, 125 };
    static readonly int[] Multiplicities = { 3, 2, 2, 2 };
    static readonly int[,] Permutations = { {0,1,2}, {0,2,1}, {1,0,2}, {1,2,0}, {2,0,1}, {2,1,0} };
    static readonly int[,] Addition = new int[Q,Q];
    static readonly int[] Negative = new int[Q];
    static readonly int[] Double = new int[Q];
    static readonly bool[] IsBasis = new bool[Q];
    static long LeafCount, TupleCount, FullDomainValues, AllGraphPairs, SameColorPairs;
    static long SmallCount, TrivialCount, ColoredCount, SmallFiveSubsets, AllFiveSubsets;
    static readonly SortedDictionary<int,long> CandidateHistogram = new SortedDictionary<int,long>();
    static readonly SortedDictionary<int,long> SmallCandidateHistogram = new SortedDictionary<int,long>();
    static readonly SortedDictionary<int,long> ColorsHistogram = new SortedDictionary<int,long>();
    static readonly SortedDictionary<int,long> SmallByRoot = new SortedDictionary<int,long>();
    static readonly List<Dictionary<string,object>> Exceptions = new List<Dictionary<string,object>>();
    static readonly List<Dictionary<string,object>> RootsReport = new List<Dictionary<string,object>>();
    static readonly Stopwatch Watch = new Stopwatch();
    static string Context = "initialization";

    static void Need(bool condition, string message)
    {
        if (!condition) throw new InvalidDataException(Context + ": " + message);
    }

    static int Encode(int[] x) { return x[0]+5*x[1]+25*x[2]+125*x[3]; }
    static int[] Decode(int g) { return new[] {g%5,g/5%5,g/25%5,g/125%5}; }
    static void PrepareGroup()
    {
        for (int g=0;g<Q;g++)
        {
            var a=Decode(g);
            Negative[g]=Encode(a.Select(x => (5-x)%5).ToArray());
            for (int h=0;h<Q;h++)
            {
                var b=Decode(h);
                Addition[g,h]=Encode(new[] {(a[0]+b[0])%5,(a[1]+b[1])%5,(a[2]+b[2])%5,(a[3]+b[3])%5});
            }
            Double[g]=Addition[g,g];
        }
        foreach (var e in Basis) IsBasis[e]=true;
        for (int g=0;g<Q;g++) Need(Addition[g,Negative[g]]==0, "group inverse");
    }

    // This retains every bounded coefficient tuple, even when several tuples
    // have the same sum. Thus copies at distinct sequence positions are not
    // silently treated as a square-free support set.
    sealed class State
    {
        public readonly int[] Sums;
        public readonly byte[] Lengths;
        public readonly int[] Distance;
        public readonly int ShortestNonemptyZero;
        public State(int[] sums, byte[] lengths)
        {
            Sums=sums; Lengths=lengths;
            Distance=Enumerable.Repeat(Infinite,Q).ToArray();
            int shortest=Infinite;
            for (int i=0;i<sums.Length;i++)
            {
                int sum=sums[i], length=lengths[i];
                if (length < Distance[sum]) Distance[sum]=length;
                if (sum==0 && length>0 && length<shortest) shortest=length;
            }
            ShortestNonemptyZero=shortest;
        }
        public State AppendValue(int g, int multiplicity)
        {
            int n=Sums.Length;
            var sums=new int[n*(multiplicity+1)];
            var lengths=new byte[sums.Length];
            int multiple=0;
            for (int copies=0;copies<=multiplicity;copies++)
            {
                for (int i=0;i<n;i++)
                {
                    int index=copies*n+i;
                    sums[index]=Addition[Sums[i],multiple];
                    lengths[index]=(byte)(Lengths[i]+copies);
                }
                multiple=Addition[multiple,g];
            }
            return new State(sums,lengths);
        }
    }

    static bool SafeDouble(State state,int g)
    {
        return state.Distance[Negative[g]]+1>Cutoff
            && state.Distance[Negative[Double[g]]]+2>Cutoff;
    }

    static int Canonical(int g)
    {
        var x=Decode(g);
        int smallest=Q;
        for (int k=0;k<6;k++)
        {
            int image=x[0]+5*x[1+Permutations[k,0]]+25*x[1+Permutations[k,1]]+125*x[1+Permutations[k,2]];
            if (image<smallest) smallest=image;
        }
        return smallest;
    }

    static void Increment(SortedDictionary<int,long> counter,int key,long amount=1)
    {
        counter.TryGetValue(key,out long old); counter[key]=old+amount;
    }
    static long Choose(int n,int k)
    {
        if (n<k) return 0;
        long result=1;
        for (int j=1;j<=k;j++) result=result*(n-j+1)/j;
        return result;
    }
    static int[] IntArray(JsonElement row,string key)
    {
        return row.GetProperty(key).EnumerateArray().Select(x => x.GetInt32()).ToArray();
    }
    static void EqualArray(JsonElement row,string key,IEnumerable<int> expected)
    {
        Need(IntArray(row,key).SequenceEqual(expected), "wrong " + key);
    }
    static void EqualNumber(JsonElement row,string key,long expected)
    {
        Need(row.GetProperty(key).GetInt64()==expected,"wrong " + key + "; expected " + expected);
    }
    static void EqualMap(JsonElement actual,IDictionary<int,long> expected,string label)
    {
        var a=actual.EnumerateObject().ToDictionary(p => int.Parse(p.Name),p => p.Value.GetInt64());
        Need(a.Count==expected.Count && expected.All(p => a.TryGetValue(p.Key,out long x) && x==p.Value),"wrong " + label);
    }
    static Dictionary<int,long> Nonzero(params long[] numbers)
    {
        var result=new Dictionary<int,long>();
        for (int i=0;i<numbers.Length;i++) if (numbers[i]!=0) result[11+2*i]=numbers[i];
        return result;
    }

    // Sequential input is a checked consequence of our independently generated
    // enumeration, not the source of the search domain.
    sealed class EvidenceStream : IDisposable
    {
        readonly StreamReader Reader;
        readonly string DataType;
        public JsonElement? Metadata,Summary;
        public readonly Dictionary<int,JsonElement> Roots=new Dictionary<int,JsonElement>();
        public long DataCount;
        public EvidenceStream(string path,string dataType)
        {
            Reader=new StreamReader(path,System.Text.Encoding.UTF8,true); DataType=dataType;
        }
        public JsonDocument Next()
        {
            string line;
            while ((line=Reader.ReadLine())!=null)
            {
                Need(!String.IsNullOrWhiteSpace(line),"blank evidence line");
                var doc=JsonDocument.Parse(line);
                var row=doc.RootElement;
                string type=row.GetProperty("type").GetString();
                if (type==DataType) { DataCount++; return doc; }
                if (type=="metadata") { Need(Metadata==null,"duplicate metadata"); Metadata=row.Clone(); }
                else if (type=="summary") { Need(Summary==null,"duplicate summary"); Summary=row.Clone(); }
                else if (type=="root")
                {
                    int r=row.GetProperty("root").GetInt32();
                    Need(!Roots.ContainsKey(r),"duplicate root record"); Roots[r]=row.Clone();
                }
                else { doc.Dispose(); throw new InvalidDataException("unexpected evidence type " + type); }
                doc.Dispose();
            }
            return null;
        }
        public void Dispose() { Reader.Dispose(); }
    }

    static void CheckLeaf(State state,int[] blocks,EvidenceStream scan,EvidenceStream certificates)
    {
        Context="leaf " + LeafCount + " (" + String.Join(",",blocks) + ")";
        Need(state.Sums.Length==2916,"bounded coefficient denominator");
        Need(state.ShortestNonemptyZero>Cutoff,"core itself has a forbidden zero sum");
        TupleCount+=state.Sums.Length;
        using var document=scan.Next();
        Need(document!=null,"missing source leaf");
        var row=document.RootElement;
        EqualArray(row,"blocks",blocks);
        EqualNumber(row,"root",blocks[0]);
        EqualNumber(row,"length",15);

        var hist=new SortedDictionary<int,long>();
        foreach (int d in state.Distance) Increment(hist,d);
        EqualMap(row.GetProperty("distance_counts"),hist,"full 625-target distance histogram");
        long unreachable=hist.TryGetValue(Infinite,out long unreachableCount)?unreachableCount:0;
        EqualNumber(row,"coverage",Q-unreachable);
        EqualNumber(row,"unreachable_count",unreachable);
        EqualNumber(row,"maximum_distance",state.Distance.Max());
        EqualNumber(row,"finite_maximum_distance",state.Distance.Where(d=>d<Infinite).Max());

        var safe=new List<int>();
        var outside=new List<int>();
        var safe14=new List<int>();
        // Enumerate the entire group. Zero is tested, and the support is only
        // removed after the safe single-extension condition has been evaluated.
        for (int g=0;g<Q;g++)
        {
            if (state.Distance[Negative[g]]+1>13)
            {
                safe.Add(g);
                if (!IsBasis[g] && !blocks.Contains(g)) outside.Add(g);
            }
            if (state.Distance[Negative[g]]+1>14) safe14.Add(g);
        }
        FullDomainValues+=Q;
        EqualArray(row,"safe_single_additions",safe);
        EqualArray(row,"outside_safe_additions",outside);
        EqualArray(row,"safe_single_additions_cutoff14",safe14);
        int n=outside.Count;
        long five=Choose(n,5);
        EqualNumber(row,"five_subset_count",five);
        Increment(CandidateHistogram,n);
        AllFiveSubsets+=five;
        if (n>20)
        {
            Need(n==127,"unexpected exceptional candidate count");
            Exceptions.Add(new Dictionary<string,object> { ["source_index"]=LeafCount,["root"]=blocks[0],
                ["blocks"]=blocks.ToArray(),["candidate_count"]=n });
            LeafCount++;
            return;
        }
        SmallCount++;
        SmallFiveSubsets+=five;
        Increment(SmallByRoot,blocks[0]);
        Increment(SmallCandidateHistogram,n);
        using var certificate=certificates.Next();
        Need(certificate!=null,"missing small-core certificate");
        var proof=certificate.RootElement;
        EqualNumber(proof,"source_index",LeafCount);
        EqualNumber(proof,"root",blocks[0]);
        EqualArray(proof,"blocks",blocks);
        EqualArray(proof,"outside_safe_values",outside);
        EqualNumber(proof,"candidate_count",n);
        EqualNumber(proof,"five_subset_denominator",five);
        Need(proof.GetProperty("completed_exhaustively").GetBoolean(),"incomplete certificate");
        Need(proof.GetProperty("decision_complete").GetBoolean(),"incomplete decision");
        Need(proof.GetProperty("witness_added_values").ValueKind==JsonValueKind.Null,"claimed extension witness");
        if (n<5)
        {
            TrivialCount++;
            Need(proof.GetProperty("reason").GetString()=="fewer_than_five_outside_safe_values","wrong trivial reason");
            EqualNumber(proof,"pair_checks",0);
            EqualNumber(proof,"dfs_nodes",0);
        }
        else
        {
            ColoredCount++;
            Need(!proof.GetProperty("stopped_for_time").GetBoolean(),"timed out certificate");
            var adjacency=new int[n];
            for (int i=0;i<n;i++) for (int j=i+1;j<n;j++)
            {
                AllGraphPairs++;
                int target=Negative[Addition[outside[i],outside[j]]];
                if (state.Distance[target]+2>13)
                {
                    adjacency[i]|=1<<j; adjacency[j]|=1<<i;
                }
            }
            EqualArray(proof,"adjacency_bitmasks",adjacency);
            EqualNumber(proof,"pair_checks",Choose(n,2));
            EqualNumber(proof,"dfs_nodes",1);
            var colors=IntArray(proof,"root_proper_color_classes");
            Need(colors.Length>=1 && colors.Length<=4,"not a coloring with at most four colors");
            Increment(ColorsHistogram,colors.Length);
            int full=(1<<n)-1,covered=0;
            foreach (int color in colors)
            {
                Need(color>0 && (color&~full)==0,"empty or out-of-range color class");
                Need((covered&color)==0,"overlapping color classes");
                covered|=color;
                for (int i=0;i<n;i++) if ((color&(1<<i))!=0)
                    for (int j=i+1;j<n;j++) if ((color&(1<<j))!=0)
                    {
                        SameColorPairs++;
                        int target=Negative[Addition[outside[i],outside[j]]];
                        Need(state.Distance[target]+2<=13,"same-color pair is compatible");
                    }
            }
            Need(covered==full,"uncolored vertices");
        }
        LeafCount++;
        if (LeafCount%10000==0)
            Console.WriteLine(JsonSerializer.Serialize(new { verified_cores=LeafCount,seconds=Watch.Elapsed.TotalSeconds }));
    }

    static string Hash(string path)
    {
        using var stream=File.OpenRead(path);
        using var sha=SHA256.Create();
        return Convert.ToHexString(sha.ComputeHash(stream)).ToLowerInvariant();
    }

    static void CheckRoot(JsonElement row,int root,long n13,long n15,long n17,long leaf11,long leaf13,long leaf15,bool target17)
    {
        Context="root " + root + (target17?" original target17":" scan target15");
        Need(row.GetProperty("completed_exhaustively").GetBoolean(),"incomplete root");
        EqualMap(row.GetProperty("nodes_by_length"),target17?Nonzero(1,n13,n15,n17):Nonzero(1,n13,n15),"nodes by length");
        EqualMap(row.GetProperty("leaves_by_length"),target17?Nonzero(leaf11,leaf13,leaf15):Nonzero(leaf11,leaf13),"leaves by length");
        EqualNumber(row,"nodes",1+n13+n15+(target17?n17:0));
        EqualNumber(row,"terminal_count",target17?n17:n15);
        int maximum=target17&&n17>0?17:n15>0?15:n13>0?13:11;
        EqualNumber(row,"max_reached_length",maximum);
    }

    static void CheckMetadata(JsonElement metadata,int target,List<int> initial,List<int> roots)
    {
        Need(metadata.GetProperty("mode").GetString()=="3222","wrong metadata mode");
        Need(metadata.GetProperty("group").GetString()=="C_5^4","wrong metadata group");
        EqualNumber(metadata,"m",Cutoff);
        EqualNumber(metadata,"target",target);
        EqualNumber(metadata,"core_length",9);
        EqualNumber(metadata,"block_multiplicity",2);
        EqualNumber(metadata,"new_blocks",(target-9)/2);
        EqualNumber(metadata,"initial_safe_count",initial.Count);
        EqualArray(metadata,"initial_safe_candidates",initial);
        EqualArray(metadata,"canonical_roots",roots);
    }

    static Dictionary<string,object> Execute(string directory)
    {
        Watch.Start();
        PrepareGroup();
        string originalPath=Path.Combine(directory,"evidence/atom_3222_m13_blocks.jsonl");
        string scanPath=Path.Combine(directory,"evidence/atom_3222_len15_scan.jsonl");
        string coresPath=Path.Combine(directory,"evidence/finite_single_extension_trial_cores.jsonl");
        string trialPath=Path.Combine(directory,"evidence/finite_single_extension_trial.json");
        var inputs=new Dictionary<string,string>();
        foreach (var path in new[] { originalPath,scanPath,coresPath,trialPath })
            inputs[Path.GetRelativePath(directory,path).Replace('\\','/')]=Hash(path);
        using var original=new EvidenceStream(originalPath,"unused");
        Need(original.Next()==null,"unexpected original data record");
        Need(original.Metadata!=null && original.Summary!=null,"missing original boundary records");
        using var scan=new EvidenceStream(scanPath,"leaf_profile");
        using var certificates=new EvidenceStream(coresPath,"core_result");
        using var trialDocument=JsonDocument.Parse(File.ReadAllText(trialPath));
        var trial=trialDocument.RootElement;
        var baseState=new State(new[] {0},new byte[] {0});
        for (int i=0;i<Basis.Length;i++) baseState=baseState.AppendValue(Basis[i],Multiplicities[i]);
        Need(baseState.Sums.Length==108 && baseState.ShortestNonemptyZero>13,"base coefficient enumeration");
        var initial=new List<int>();
        for (int g=0;g<Q;g++) if (!IsBasis[g] && SafeDouble(baseState,g)) initial.Add(g);
        var roots=initial.Where(g=>Canonical(g)==g).ToList();
        Need(initial.Count==430 && roots.Count==106,"initial orbit denominator");
        Need(initial.All(g=>roots.Contains(Canonical(g))),"uncovered safe initial orbit");
        CheckMetadata(original.Metadata.Value,17,initial,roots);
        long total13=0,total17=0,totalLeaves13=0,totalLeaves15=0;
        var expectedRootStats=new Dictionary<int,long[]>();
        foreach (int root in roots.AsEnumerable().Reverse())
        {
            Context="rebuilding root " + root;
            var first=baseState.AppendValue(root,2);
            Need(first.ShortestNonemptyZero>13,"unsafe canonical root");
            long n13=0,n15=0,n17=0,leaf13=0,leaf15=0;
            // Every candidate comes from the full 625-element domain. No
            // producer candidate list, scan list, or prior cache prunes it.
            for (int second=root+1;second<Q;second++)
            {
                if (IsBasis[second] || !SafeDouble(first,second)) continue;
                n13++;
                var next=first.AppendValue(second,2);
                Need(next.ShortestNonemptyZero>13,"unsafe second block");
                long children=0;
                for (int third=second+1;third<Q;third++)
                {
                    if (IsBasis[third] || !SafeDouble(next,third)) continue;
                    children++; n15++;
                    var leaf=next.AppendValue(third,2);
                    CheckLeaf(leaf,new[] {root,second,third},scan,certificates);
                    long terminals=0;
                    for (int fourth=third+1;fourth<Q;fourth++)
                        if (!IsBasis[fourth] && SafeDouble(leaf,fourth)) terminals++;
                    n17+=terminals;
                    if (terminals==0) leaf15++;
                }
                if (children==0) leaf13++;
            }
            long leaf11=n13==0?1:0;
            Need(original.Roots.ContainsKey(root),"missing original root");
            CheckRoot(original.Roots[root],root,n13,n15,n17,leaf11,leaf13,leaf15,true);
            expectedRootStats[root]=new[] {n13,n15,n17,leaf11,leaf13,leaf15};
            total13+=n13; total17+=n17; totalLeaves13+=leaf13; totalLeaves15+=leaf15;
            RootsReport.Add(new Dictionary<string,object> { ["root"]=root,["length11"]=1,["length13"]=n13,
                ["length15"]=n15,["length17"]=n17,["terminal_length13"]=leaf13,["terminal_length15"]=leaf15 });
        }
        Context="final exhaustive coverage";
        Need(scan.Next()==null,"extra source leaf outside independently generated tree");
        Need(certificates.Next()==null,"extra small-core certificate");
        Need(scan.Metadata!=null && scan.Summary!=null && certificates.Metadata!=null && certificates.Summary!=null,"missing evidence boundary records");
        CheckMetadata(scan.Metadata.Value,15,initial,roots);
        Need(original.Roots.Keys.OrderBy(x=>x).SequenceEqual(roots),"original root set mismatch");
        Need(scan.Roots.Keys.OrderBy(x=>x).SequenceEqual(roots),"scan root set mismatch");
        foreach (var pair in expectedRootStats)
        {
            var s=pair.Value;
            CheckRoot(scan.Roots[pair.Key],pair.Key,s[0],s[1],s[2],s[3],s[4],s[5],false);
        }
        Context="summary binding";
        Need(LeafCount==107656 && scan.DataCount==LeafCount,"length15 denominator");
        Need(SmallCount==107647 && certificates.DataCount==SmallCount && Exceptions.Count==9,"small/exceptional partition");
        Need(TrivialCount==28781 && ColoredCount==78866,"exclusion split");
        Need(AllGraphPairs==3504311 && SmallFiveSubsets==47953716,"pair/five-subset denominators");
        foreach (var end in new[] {original.Summary.Value,scan.Summary.Value})
        {
            Need(end.GetProperty("all_roots_completed").GetBoolean(),"incomplete source summary");
            EqualNumber(end,"canonical_root_count",roots.Count);
            EqualNumber(end,"attempted_roots",roots.Count);
            EqualNumber(end,"completed_roots_this_run",roots.Count);
        }
        EqualNumber(original.Summary.Value,"nodes_this_run",roots.Count+total13+LeafCount+total17);
        EqualNumber(original.Summary.Value,"terminal_count",total17);
        EqualNumber(scan.Summary.Value,"nodes_this_run",roots.Count+total13+LeafCount);
        EqualNumber(scan.Summary.Value,"terminal_count",LeafCount);
        EqualNumber(scan.Summary.Value,"leaf_profile_count",LeafCount);
        EqualNumber(scan.Summary.Value,"five_subset_denominator",AllFiveSubsets);
        EqualMap(scan.Summary.Value.GetProperty("outside_safe_count_distribution"),CandidateHistogram,"scan histogram");
        EqualNumber(certificates.Metadata.Value,"eligible_cores",SmallCount);
        EqualNumber(certificates.Metadata.Value,"cutoff",13);
        EqualNumber(certificates.Metadata.Value,"max_outside_candidates",20);
        EqualNumber(certificates.Summary.Value,"completed_cores",SmallCount);
        EqualNumber(certificates.Summary.Value,"eligible_cores",SmallCount);
        EqualNumber(certificates.Summary.Value,"total_dfs_nodes",ColoredCount);
        EqualNumber(trial,"input_length15_cores",LeafCount);
        EqualNumber(trial,"input_root_count",roots.Count);
        EqualNumber(trial,"eligible_cores",SmallCount);
        EqualNumber(trial,"completed_cores",SmallCount);
        EqualNumber(trial,"processed_cores",SmallCount);
        EqualNumber(trial,"trivial_fewer_than5_cores",TrivialCount);
        EqualNumber(trial,"root_coloring_excluded_cores",ColoredCount);
        EqualNumber(trial,"total_pair_checks",AllGraphPairs);
        EqualNumber(trial,"total_dfs_nodes",ColoredCount);
        EqualNumber(trial,"five_subset_denominator",SmallFiveSubsets);
        EqualNumber(trial,"processed_five_subset_denominator",SmallFiveSubsets);
        EqualMap(trial.GetProperty("candidate_count_distribution"),SmallCandidateHistogram,"trial histogram");
        EqualMap(trial.GetProperty("eligible_cores_by_root"),SmallByRoot,"eligible roots");
        EqualMap(trial.GetProperty("completed_cores_by_root"),SmallByRoot,"completed roots");
        var claimedExceptions=trial.GetProperty("excluded_cores").EnumerateArray().ToArray();
        Need(claimedExceptions.Length==Exceptions.Count,"exceptional core denominator");
        for (int i=0;i<Exceptions.Count;i++)
        {
            var actual=Exceptions[i]; var claim=claimedExceptions[i];
            EqualNumber(claim,"source_index",(long)actual["source_index"]);
            EqualNumber(claim,"root",(int)actual["root"]);
            EqualNumber(claim,"candidate_count",127);
            EqualArray(claim,"blocks",(int[])actual["blocks"]);
        }
        Need(trial.GetProperty("core_records_sha256").GetString()==inputs["evidence/finite_single_extension_trial_cores.jsonl"],"trial certificate file hash");
        Need(trial.GetProperty("input_sha256").GetProperty("evidence/atom_3222_len15_scan.jsonl").GetString()==inputs["evidence/atom_3222_len15_scan.jsonl"],"trial source hash");
        Need(trial.GetProperty("witness").ValueKind==JsonValueKind.Null,"unexpected trial witness");
        foreach (var input in inputs) Need(Hash(Path.Combine(directory,input.Key))==input.Value,"input modified during audit");
        return new Dictionary<string,object> {
            ["status"]="CORRECT_FOR_COMPLETE_CORE_COVERAGE_AND_107647_SMALL_CORES",
            ["local_target"]="a=1,b=6; the nine dense12 cores require the separately bound fresh audit",
            ["independence"]="No producer or prior verifier imported. Direct bounded coefficient enumeration, not a producer subset-sum engine.",
            ["group_order"]=Q,["avoidance_cutoff"]=Cutoff,["initial_safe_double_values"]=initial.Count,
            ["canonical_roots"]=roots,["root_count"]=roots.Count,["length13_nodes"]=total13,
            ["length15_cores"]=LeafCount,["length17_nodes"]=total17,["length13_leaves"]=totalLeaves13,
            ["length15_leaves_in_original_tree"]=totalLeaves15,["bounded_coefficient_tuples_per_core"]=2916,
            ["bounded_coefficient_tuples_checked"]=TupleCount,["position_subsets_represented_per_core"]=32768,
            ["full_domain_candidate_values_checked"]=FullDomainValues,["all_small_cores"]=SmallCount,
            ["fewer_than_five_candidates"]=TrivialCount,["colored_cores"]=ColoredCount,
            ["graph_pairs_recomputed"]=AllGraphPairs,["same_color_pairs_directly_rechecked"]=SameColorPairs,
            ["color_count_histogram"]=ColorsHistogram,["candidate_count_histogram"]=CandidateHistogram,
            ["small_core_five_subset_denominator"]=SmallFiveSubsets,["all_core_five_subset_denominator"]=AllFiveSubsets,
            ["exceptional_cores"]=Exceptions,["root_counts"]=RootsReport,["input_sha256"]=inputs,
            ["verifier_sha256"]=Hash(Path.Combine(directory,"scripts/verify_single_extensions_fresh.cs")),
            ["runner_sha256"]=Hash(Path.Combine(directory,"scripts/verify_single_extensions_fresh.ps1")),
            ["runtime"]=System.Runtime.InteropServices.RuntimeInformation.FrameworkDescription,
            ["seconds"]=Watch.Elapsed.TotalSeconds
        };
    }

    public static void Run(string directory,string output)
    {
        try
        {
            var result=Execute(directory);
            File.WriteAllText(output,JsonSerializer.Serialize(result,new JsonSerializerOptions {WriteIndented=true})+Environment.NewLine,new System.Text.UTF8Encoding(false));
            Console.WriteLine(JsonSerializer.Serialize(new { status=result["status"],cores=LeafCount,small_cores=SmallCount,
                same_color_pairs=SameColorPairs,seconds=Watch.Elapsed.TotalSeconds,output }));
        }
        catch (Exception error)
        {
            File.WriteAllText(output,JsonSerializer.Serialize(new {status="CRITICAL_GAPS_OR_CHECKER_FAILURE",context=Context,error=error.ToString()},new JsonSerializerOptions {WriteIndented=true})+Environment.NewLine,new System.Text.UTF8Encoding(false));
            throw;
        }
    }
}
