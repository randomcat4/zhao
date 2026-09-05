// Fresh-context verifier. No imports from any producer or previous checker.
// Distances are reconstructed from ALL 3^k coefficient tuples, not DP updates.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

public static class VerifySevenFreshCore {
    const int Q = 625;
    static readonly int[] basis = {1, 5, 25, 125};
    static readonly int[] sumTable = new int[Q*Q];
    static readonly int[] negative = new int[Q];
    static readonly int[] doubled = new int[Q];
    static readonly int[,] coord = new int[Q,4];
    static readonly int[] baseSums = new int[81];
    static readonly int[] baseLengths = new int[81];
    static long coefficientTuples = 0;
    static int Add(int x, int y) {
        int r = 0, place = 1;
        for (int k=0;k<4;k++,place*=5) {
            r += ((x%5 + y%5)%5)*place;
            x/=5; y/=5;
        }
        return r;
    }
    static void Require(bool condition, string message) {
        if (!condition) throw new Exception(message);
    }
    static int[] IntArray(JsonElement j) {return j.EnumerateArray().Select(x=>x.GetInt32()).ToArray();}
    static string Hash(string path) {return Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path))).ToLowerInvariant();}
    static void Initialize() {
        for(int x=0;x<Q;x++) {
            int v=x;
            for(int k=0;k<4;k++){coord[x,k]=v%5;v/=5;}
            for(int y=0;y<Q;y++)sumTable[x*Q+y]=Add(x,y);
            doubled[x]=Add(x,x);
            negative[x]=0;
            int p=1;
            for(int k=0;k<4;k++,p*=5)negative[x]+=((5-coord[x,k])%5)*p;
            Require(Add(x,negative[x])==0,"additive inverse");
        }
        for(int i=0;i<81;i++) {
            int n=i,s=0,l=0,p=1;
            for(int k=0;k<4;k++,p*=5){int a=n%3;n/=3;s+=a*p;l+=a;}
            baseSums[i]=s;baseLengths[i]=l;
        }
    }
    // Enumerate each extra coefficient independently and then all 81 basis
    // coefficients. Every support multiplicity is exactly 0, 1, or 2.
    static void EnumeratedDistances(byte[] distance, params int[] extra) {
        Array.Fill(distance,(byte)99);
        int tuples=1;
        foreach(int unused in extra)tuples*=3;
        for(int i=0;i<tuples;i++) {
            int n=i,s=0,l=0;
            foreach(int g in extra) {
                int a=n%3;n/=3;l+=a;
                if(a!=0)s=sumTable[s*Q+(a==1?g:doubled[g])];
            }
            for(int j=0;j<81;j++) {
                int target=sumTable[s*Q+baseSums[j]], length=l+baseLengths[j];
                Require(target!=0 || length==0 || length>13,"enumerated short zero");
                if(length<distance[target])distance[target]=(byte)length;
                coefficientTuples++;
            }
        }
    }
    static bool IsSafeDouble(byte[] distance,int x) {
        return distance[negative[x]]>12 && distance[negative[doubled[x]]]>11;
    }
    static int Canonical(int x) {
        int best=Q;
        for(int a=0;a<4;a++)for(int b=0;b<4;b++)if(b!=a)
        for(int c=0;c<4;c++)if(c!=a&&c!=b)
        for(int d=0;d<4;d++)if(d!=a&&d!=b&&d!=c) {
            int v=coord[x,a]+5*coord[x,b]+25*coord[x,c]+125*coord[x,d];
            best=Math.Min(best,v);
        }
        return best;
    }
    static long Choose(int n,int k) {
        if(n<k)return 0;
        long c=1;
        for(int j=1;j<=k;j++)c=checked(c*(n-j+1))/j;
        return c;
    }
    static Dictionary<string,long> Sparse(long[] a) {
        var r=new Dictionary<string,long>();
        for(int i=0;i<a.Length;i++)if(a[i]!=0)r[i.ToString()]=a[i];
        return r;
    }
    static void CheckHistogram(JsonElement input,long[] actual,string label) {
        var supplied=new Dictionary<int,long>();
        foreach(var p in input.EnumerateObject())supplied.Add(int.Parse(p.Name),p.Value.GetInt64());
        Require(supplied.Count==actual.Count(x=>x>0),label+" cardinality");
        foreach(var p in supplied)Require(p.Key>=0&&p.Key<actual.Length&&actual[p.Key]==p.Value,label+" entry");
    }
    public static void Run(string directory) {
        var timer=Stopwatch.StartNew();
        string[] inputFiles={
            "proofs/seven_doubles_continue.md", "evidence/seven_doubles_continue_frozen_manifest.json",
            "evidence/seven_doubles_continue_probe.json", "evidence/seven_doubles_continue_probe_cores.jsonl",
            "evidence/atom_2222_m13_blocks.jsonl", "scripts/seven_doubles_continue_probe.cs",
            "scripts/atom_double_blocks.ps1", "scripts/verify_seven_fresh_core.cs",
            "scripts/verify_seven_fresh_core.ps1"
        };
        var hashes=inputFiles.ToDictionary(p=>p,p=>Hash(Path.Combine(directory,p)));
        using var probeDoc=JsonDocument.Parse(File.ReadAllText(Path.Combine(directory,inputFiles[2]),Encoding.UTF8));
        var probe=probeDoc.RootElement;
        Require(probe.GetProperty("status").GetString()=="COMPLETE_PROBE_WITH_EXACT_COLORING_RESIDUAL","producer completion");
        Require(probe.GetProperty("input_sha256").GetString()==hashes[inputFiles[4]],"probe prior binding");
        Require(probe.GetProperty("producer_sha256").GetString()==hashes[inputFiles[5]],"probe source binding");
        Require(probe.GetProperty("original_script_sha256").GetString()==hashes[inputFiles[6]],"probe old source binding");
        Initialize();
        var fixedD=new byte[Q];EnumeratedDistances(fixedD);
        var initial=new List<int>();
        for(int x=0;x<Q;x++)if(!basis.Contains(x)&&IsSafeDouble(fixedD,x))initial.Add(x);
        var roots=initial.Select(Canonical).Distinct().OrderBy(x=>x).ToArray();
        Require(initial.Count==475&&roots.Length==44,"initial/root counts");
        var oldCounts=new Dictionary<int,long>();
        using(var old=new StreamReader(Path.Combine(directory,inputFiles[4]),Encoding.UTF8)) {
            using(var metaDoc=JsonDocument.Parse(old.ReadLine())) {
                var meta=metaDoc.RootElement;
                Require(IntArray(meta.GetProperty("initial_safe_candidates")).SequenceEqual(initial),"old initial list");
                Require(IntArray(meta.GetProperty("canonical_roots")).SequenceEqual(roots),"old roots");
                Require(meta.GetProperty("script_sha256").GetString()==hashes[inputFiles[6]],"old source binding");
            }
            string line;
            while((line=old.ReadLine())!=null) {
                using var doc=JsonDocument.Parse(line);var j=doc.RootElement;
                if(j.GetProperty("type").GetString()!="root")continue;
                Require(j.GetProperty("completed_exhaustively").GetBoolean(),"old unfinished root");
                oldCounts.Add(j.GetProperty("root").GetInt32(),j.GetProperty("nodes_by_length").GetProperty("14").GetInt64());
            }
        }
        Require(oldCounts.Keys.OrderBy(x=>x).SequenceEqual(roots),"old root denominator");
        var candHist=new long[626];var colorHist=new long[626];var counts=new Dictionary<int,long>();
        var residual=new List<int[]>();
        long coreCount=0,pairCount=0,colored=0,six=0,seven=0,resSix=0,resSeven=0,secondCount=0;
        var d10=new byte[Q];var d12=new byte[Q];var d14=new byte[Q];
        using(var rows=new StreamReader(Path.Combine(directory,inputFiles[3]),Encoding.UTF8)) {
            using(var metadataDoc=JsonDocument.Parse(rows.ReadLine())) {
                var m=metadataDoc.RootElement;
                Require(m.GetProperty("type").GetString()=="metadata","core metadata");
                Require(m.GetProperty("cutoff").GetInt32()==13&&m.GetProperty("core_length").GetInt32()==14,"length contract");
                Require(m.GetProperty("expected_cores").GetInt32()==166195,"expected cores");
                Require(IntArray(m.GetProperty("fixed_sequence")).SequenceEqual(basis.SelectMany(x=>new[]{x,x})),"fixed basis");
                Require(IntArray(m.GetProperty("canonical_roots")).SequenceEqual(roots),"core root metadata");
                Require(m.GetProperty("input_sha256").GetString()==hashes[inputFiles[4]],"core input binding");
                Require(m.GetProperty("original_script_sha256").GetString()==hashes[inputFiles[6]],"core old source binding");
                Require(m.GetProperty("producer_sha256").GetString()==hashes[inputFiles[5]],"core producer binding");
            }
            foreach(int a in roots) {
                EnumeratedDistances(d10,a);long thisRoot=0;
                // Each level loops over the whole group above its ordering floor.
                // It never inherits the producer's initial candidate list.
                for(int b=a+1;b<Q;b++) {
                    if(basis.Contains(b)||!IsSafeDouble(d10,b))continue;
                    EnumeratedDistances(d12,a,b);secondCount++;
                    for(int c=b+1;c<Q;c++) {
                        if(basis.Contains(c)||!IsSafeDouble(d12,c))continue;
                        EnumeratedDistances(d14,a,b,c);
                        string line=rows.ReadLine();Require(line!=null,"missing core line");
                        using var rowDoc=JsonDocument.Parse(line);var j=rowDoc.RootElement;
                        Require(j.GetProperty("type").GetString()=="core","premature trailer");
                        Require(j.GetProperty("index").GetInt64()==coreCount,"core index");
                        Require(IntArray(j.GetProperty("blocks")).SequenceEqual(new[]{a,b,c}),"key coverage");
                        var candidates=new List<int>();
                        for(int x=0;x<Q;x++)if(x!=a&&x!=b&&x!=c&&!basis.Contains(x)&&d14[negative[x]]>12)candidates.Add(x);
                        Require(IntArray(j.GetProperty("candidates")).SequenceEqual(candidates),"all-domain candidate mismatch");
                        int n=candidates.Count;
                        var colors=IntArray(j.GetProperty("colors"));
                        int k=j.GetProperty("color_count").GetInt32();
                        Require(colors.Length==n&&k>=0&&k<=n,"color dimensions");
                        Require(colors.All(x=>x>=0&&x<k)&&colors.Distinct().Count()==k,"color labels");
                        for(int p=0;p<n;p++)for(int q=p+1;q<n;q++) {
                            int target=negative[sumTable[candidates[p]*Q+candidates[q]]];
                            bool edge=d14[target]>11;
                            Require(!edge||colors[p]!=colors[q],"invalid coloring");
                            pairCount++;
                        }
                        Require(j.GetProperty("pair_checks").GetInt64()==(long)n*(n-1)/2,"pair denominator");
                        long s6=Choose(n,6),s7=Choose(n,7);
                        Require(j.GetProperty("six_subset_count").GetInt64()==s6&&j.GetProperty("seven_subset_count").GetInt64()==s7,"combination counts");
                        Require(j.GetProperty("no_six_extension_by_coloring").GetBoolean()==(k<=5),"claimed exclusion");
                        if(k<=5)colored++;
                        else{residual.Add(new[]{a,b,c});resSix+=s6;resSeven+=s7;}
                        coreCount++;thisRoot++;six+=s6;seven+=s7;candHist[n]++;colorHist[k]++;
                    }
                }
                Require(thisRoot==oldCounts[a],"per-root old count");counts.Add(a,thisRoot);
                Require(probe.GetProperty("generated_cores_by_root").GetProperty(a.ToString()).GetInt64()==thisRoot,"per-root producer count");
            }
            using var trailerDoc=JsonDocument.Parse(rows.ReadLine());var t=trailerDoc.RootElement;
            Require(t.GetProperty("type").GetString()=="summary","missing trailer");
            Require(t.GetProperty("processed_cores").GetInt64()==coreCount&&t.GetProperty("colored_cores").GetInt64()==colored,"trailer count");
            Require(t.GetProperty("residual_cores").GetInt64()==residual.Count&&!t.GetProperty("time_limit_reached").GetBoolean(),"trailer incomplete");
            Require(string.IsNullOrWhiteSpace(rows.ReadToEnd()),"extra certificate records");
        }
        Require(coreCount==166195&&secondCount==8642&&colored==166180&&residual.Count==15,"complete result counts");
        Require(pairCount==35295586,"pair checks");
        Require(probe.GetProperty("processed_cores").GetInt64()==coreCount&&probe.GetProperty("colored_cores").GetInt64()==colored,"probe counts");
        Require(probe.GetProperty("residual_cores").GetInt64()==residual.Count&&probe.GetProperty("unprocessed_cores").GetInt64()==0,"probe residual count");
        Require(!probe.GetProperty("time_limit_reached").GetBoolean(),"probe incomplete");
        CheckHistogram(probe.GetProperty("candidate_histogram"),candHist,"candidate histogram");
        CheckHistogram(probe.GetProperty("color_histogram"),colorHist,"color histogram");
        var suppliedResidual=probe.GetProperty("residual_keys").EnumerateArray().Select(IntArray).ToArray();
        Require(suppliedResidual.Length==residual.Count&&suppliedResidual.Zip(residual,(x,y)=>x.SequenceEqual(y)).All(x=>x),"residual keys");
        foreach(var pair in new[]{("six_subset_denominator",six),("seven_subset_denominator",seven),("residual_six_subset_denominator",resSix),("residual_seven_subset_denominator",resSeven)})
            Require(long.Parse(probe.GetProperty(pair.Item1).GetString())==pair.Item2,"aggregate subset counts");
        Require(probe.GetProperty("pair_checks").GetInt64()==pairCount,"probe pair count");
        Require(Enumerable.Range(46,205).All(x=>candHist[x]==0)&&candHist[251]==15&&Enumerable.Range(252,374).All(x=>candHist[x]==0),"candidate gap");
        foreach(var p in hashes)Require(Hash(Path.Combine(directory,p.Key))==p.Value,"input changed during check: "+p.Key);
        var output=new {
            status="INDEPENDENT_COEFFICIENT_ENUMERATION_FULL_PASS",
            implementation="No imported producer or old checker; all 3^7 coefficient tuples at every accepted 14-position core",
            initial_safe_candidates=initial,canonical_roots=roots,length12_cores=secondCount,length14_cores=coreCount,
            by_root=counts,coefficient_tuples_enumerated=coefficientTuples,
            all_group_candidate_tests=coreCount*625,all_candidate_pairs=pairCount,colored_cores=colored,
            residual_keys=residual,candidate_histogram=Sparse(candHist),color_histogram=Sparse(colorHist),
            six_subset_denominator=six,seven_subset_denominator=seven,residual_six_subset_denominator=resSix,residual_seven_subset_denominator=resSeven,
            inputs_unchanged_during_verification=true,input_sha256=hashes,seconds=timer.Elapsed.TotalSeconds
        };
        File.WriteAllText(Path.Combine(directory,"evidence/verify_seven_fresh_core.json"),JsonSerializer.Serialize(output,new JsonSerializerOptions{WriteIndented=true})+"\n",new UTF8Encoding(false));
        Console.WriteLine(JsonSerializer.Serialize(new{output.status,coreCount,pairCount,coefficientTuples,output.seconds}));
    }
}
