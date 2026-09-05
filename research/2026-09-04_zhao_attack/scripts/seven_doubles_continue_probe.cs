// Bounded producer, not an independent certification. No singleton DFS here.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Text.Json;

public static class SevenDoublesContinueProbe {
    const int Q=625, INF=99;
    static int[] plus=new int[Q*Q], neg=new int[Q], twice=new int[Q];
    static int[,] digits=new int[Q,4];
    static int[] basis={1,5,25,125};
    static int Add(int a,int b) { int z=0,p=1; for(int j=0;j<4;j++){z+=((a%5+b%5)%5)*p;a/=5;b/=5;p*=5;}return z; }
    static byte[] Append(byte[] d,int g,int copies) {
        byte[] n=(byte[])d.Clone();
        for(int h=0;h<Q;h++)for(int t=1;t<=copies;t++){
            int k=d[h]+t, p=plus[(t==1?g:twice[g])*Q+h];
            if(k<n[p])n[p]=(byte)k;
        }
        return n;
    }
    static bool Safe(byte[] d,int g) { return d[neg[g]]>=13&&d[neg[twice[g]]]>=12; }
    static int[] Greedy(bool[] a,int n,int[] order) {
        int[] color=Enumerable.Repeat(-1,n).ToArray(); bool[] forbidden=new bool[n];
        foreach(int v in order){Array.Clear(forbidden,0,n);for(int j=0;j<n;j++)if(a[v*n+j]&&color[j]>=0)forbidden[color[j]]=true;
            int c=0;while(forbidden[c])c++;color[v]=c;}
        return color;
    }
    static int[] Dsatur(bool[] a,int n,int[] degree) {
        int[] color=Enumerable.Repeat(-1,n).ToArray(),sat=new int[n];bool[] forbidden=new bool[n*n];
        for(int k=0;k<n;k++){
            int v=-1;for(int i=0;i<n;i++)if(color[i]<0&&(v<0||sat[i]>sat[v]||(sat[i]==sat[v]&&degree[i]>degree[v])))v=i;
            int c=0;while(forbidden[v*n+c])c++;color[v]=c;
            for(int i=0;i<n;i++)if(color[i]<0&&a[v*n+i]&&!forbidden[i*n+c]){forbidden[i*n+c]=true;sat[i]++;}
        }
        return color;
    }
    static int Colors(int[] color) {return color.Length==0?0:color.Max()+1;}
    static long Choose(int n,int k) {if(n<k)return 0;long x=1;for(int i=1;i<=k;i++)x=x*(n-k+i)/i;return x;}
    static Dictionary<string,long> Histogram(long[] hist){var d=new Dictionary<string,long>();for(int i=0;i<hist.Length;i++)if(hist[i]>0)d[i.ToString()]=hist[i];return d;}
    static void Write(StreamWriter w,object row){w.WriteLine(JsonSerializer.Serialize(row));}
    public static void Run(string directory,int seconds,int[] expectedRoots,int[] expectedCounts,string inputHash,string originalScriptHash,string producerHash){
        var watch=Stopwatch.StartNew();
        for(int g=0;g<Q;g++){int x=g;for(int j=0;j<4;j++){digits[g,j]=x%5;x/=5;}twice[g]=Add(g,g);neg[g]=Add(twice[g],twice[g]);for(int h=0;h<Q;h++)plus[g*Q+h]=Add(g,h);}
        byte[] core=new byte[Q];for(int g=1;g<Q;g++)core[g]=INF;foreach(int e in basis)core=Append(core,e,2);
        var initial=new List<int>();var roots=new List<int>();
        for(int g=1;g<Q;g++)if(!basis.Contains(g)&&Safe(core,g)){
            initial.Add(g);if(digits[g,0]>=digits[g,1]&&digits[g,1]>=digits[g,2]&&digits[g,2]>=digits[g,3])roots.Add(g);
        }
        if(initial.Count!=475||!roots.SequenceEqual(expectedRoots))throw new Exception("initial/root mismatch");
        var byRoot=new Dictionary<int,int>();long[] candidatesHist=new long[626],colorsHist=new long[626];
        long processed=0,pairChecks=0,colored=0;BigInteger six=0,seven=0,residualSix=0,residualSeven=0;
        var residualKeys=new List<int[]>();bool timedOut=false;
        string output=Path.Combine(directory,"seven_doubles_continue_probe_cores.jsonl");
        using(var w=new StreamWriter(output,false,new UTF8Encoding(false))){
            Write(w,new {type="metadata",role="producer; independent verification required",cutoff=13,core_length=14,
                fixed_sequence=new[]{1,1,5,5,25,25,125,125},canonical_roots=roots,expected_cores=166195,
                input_sha256=inputHash,original_script_sha256=originalScriptHash,producer_sha256=producerHash,
                certificate="candidate values and explicit proper coloring; edge iff d(-(g+h))>=12"});
            foreach(int root in roots){
                if(timedOut)break;int rootCount=0;var d10=Append(core,root,2);
                foreach(int second in initial){
                    if(second<=root||!Safe(d10,second))continue;
                    var d12=Append(d10,second,2);
                    foreach(int third in initial){
                        if(third<=second||!Safe(d12,third))continue;
                        if((processed&255)==0&&watch.Elapsed.TotalSeconds>=seconds){timedOut=true;break;}
                        byte[] d=Append(d12,third,2);int[] blocks={root,second,third};
                        var values=new List<int>();
                        for(int g=0;g<Q;g++)if(d[neg[g]]>=13&&!basis.Contains(g)&&!blocks.Contains(g))values.Add(g);
                        int n=values.Count;bool[] a=new bool[n*n];int[] degree=new int[n];
                        for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(d[neg[plus[values[i]*Q+values[j]]]]>=12){a[i*n+j]=a[j*n+i]=true;degree[i]++;degree[j]++;}
                        pairChecks+=(long)n*(n-1)/2;
                        int[] order=Enumerable.Range(0,n).ToArray(),color=Greedy(a,n,order);string method="ascending_first_fit";
                        if(Colors(color)>5){
                            Array.Sort(order,(x,y)=>degree[y]!=degree[x]?degree[y].CompareTo(degree[x]):x.CompareTo(y));
                            var c=Greedy(a,n,order);if(Colors(c)<Colors(color)){color=c;method="descending_degree_first_fit";}
                        }
                        if(Colors(color)>5){var c=Dsatur(a,n,degree);if(Colors(c)<Colors(color)){color=c;method="dsatur";}}
                        int k=Colors(color);for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(color[i]==color[j]&&a[i*n+j])throw new Exception("improper coloring");
                        bool excluded=k<=5;long c6=Choose(n,6),c7=Choose(n,7);six+=c6;seven+=c7;
                        processed++;rootCount++;candidatesHist[n]++;colorsHist[k]++;
                        if(excluded)colored++;else{residualKeys.Add(blocks);residualSix+=c6;residualSeven+=c7;}
                        Write(w,new {type="core",index=processed-1,blocks=blocks,candidates=values,colors=color,color_count=k,
                            method=method,pair_checks=(long)n*(n-1)/2,six_subset_count=c6,seven_subset_count=c7,
                            no_six_extension_by_coloring=excluded});
                    }
                    if(timedOut)break;
                }
                byRoot[root]=rootCount;
                int expected=expectedCounts[Array.IndexOf(expectedRoots,root)];
                if(!timedOut&&rootCount!=expected)throw new Exception("length14 root mismatch");
            }
            Write(w,new {type="summary",processed_cores=processed,colored_cores=colored,residual_cores=residualKeys.Count,time_limit_reached=timedOut});
        }
        bool complete=!timedOut&&processed==166195&&byRoot.Count==44;
        var summary=new {status=complete?"COMPLETE_PROBE_WITH_EXACT_COLORING_RESIDUAL":"INCOMPLETE_TIME_LIMIT",
            role="producer; independent verification required",cutoff=13,expected_cores=166195,processed_cores=processed,
            root_counts_match_input=complete,generated_cores_by_root=byRoot,time_limit_reached=timedOut,
            seconds_limit=seconds,seconds=watch.Elapsed.TotalSeconds,colored_cores=colored,residual_cores=residualKeys.Count,
            unprocessed_cores=166195-processed,pair_checks=pairChecks,candidate_histogram=Histogram(candidatesHist),
            color_histogram=Histogram(colorsHist),six_subset_denominator=six.ToString(),seven_subset_denominator=seven.ToString(),
            residual_six_subset_denominator=residualSix.ToString(),residual_seven_subset_denominator=residualSeven.ToString(),
            residual_keys=residualKeys,input_sha256=inputHash,original_script_sha256=originalScriptHash,producer_sha256=producerHash};
        string json=JsonSerializer.Serialize(summary,new JsonSerializerOptions {WriteIndented=true});
        File.WriteAllText(Path.Combine(directory,"seven_doubles_continue_probe.json"),json+"\n",new UTF8Encoding(false));
        Console.WriteLine(JsonSerializer.Serialize(new {summary.status,processed_cores=processed,colored_cores=colored,residual_cores=residualKeys.Count,summary.seconds,pairChecks}));
    }
}
