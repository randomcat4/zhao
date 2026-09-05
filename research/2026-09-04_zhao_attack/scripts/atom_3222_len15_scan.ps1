param(
    [ValidateSet('3222')][string]$Mode = '3222',
    [int]$Cutoff = 13,
    [int]$Target = 15,
    [string]$OutputFile = '',
    [string]$SkipEvidence = '',
    [int]$Seconds = 45,
    [long]$NodeLimit = 2000000
)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$atomBlockSource = @'
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;
public static class Atom3222Length15Scan {
    const int Q=625, INF=99;
    static int M,BLOCKS,coreLength;
    static int[] plus=new int[Q*Q],neg=new int[Q],twice=new int[Q],path=new int[7],longest,firstTerminal;
    static int[,] digits=new int[Q,4];
    static long[] levels=new long[8],leaves=new long[8];
    static long nodes,nodeLimit,terminals;
    static int maxDepth;
    static bool complete;
    static Stopwatch watch;
    static double deadline;
    static StreamWriter evidenceWriter;
    static long leafProfiles;
    static long fiveSubsetDenominator;
    static int largestOutside;
    static SortedDictionary<int,long> outsideHistogram=new SortedDictionary<int,long>();
    static long ChooseFive(int n){if(n<5)return 0;long v=1;for(int i=1;i<=5;i++)v=v*(n-i+1)/i;return v;}
    static string OutsideHistogram(){var s=new StringBuilder("{");bool first=true;foreach(var pair in outsideHistogram){if(!first)s.Append(',');s.Append('"').Append(pair.Key).Append("\":").Append(pair.Value);first=false;}return s.Append('}').ToString();}
    static void Profile(byte[] d,int depth){
        var safe=new List<int>();var safe14=new List<int>();int[] hist=new int[100];int maximum=0,finiteMaximum=0;
        for(int h=0;h<Q;h++){hist[d[h]]++;maximum=Math.Max(maximum,d[h]);if(d[h]<INF)finiteMaximum=Math.Max(finiteMaximum,d[h]);}
        for(int g=0;g<Q;g++){if(d[neg[g]]>=M)safe.Add(g);if(d[neg[g]]>=14)safe14.Add(g);}
        var counts=new StringBuilder("{");bool first=true;for(int k=0;k<hist.Length;k++)if(hist[k]>0){if(!first)counts.Append(',');counts.Append('"').Append(k).Append("\":").Append(hist[k]);first=false;}counts.Append('}');
        int[] blocks=new int[depth];Array.Copy(path,blocks,depth);leafProfiles++;
        var outside=new List<int>();foreach(int g in safe)if(g!=1&&g!=5&&g!=25&&g!=125&&Array.IndexOf(blocks,g)<0)outside.Add(g);
        long combinations=ChooseFive(outside.Count);fiveSubsetDenominator+=combinations;largestOutside=Math.Max(largestOutside,outside.Count);if(!outsideHistogram.ContainsKey(outside.Count))outsideHistogram[outside.Count]=0;outsideHistogram[outside.Count]++;
        evidenceWriter.WriteLine("{\"type\":\"leaf_profile\",\"root\":"+path[0]+",\"blocks\":"+Ints(blocks)+",\"length\":"+(coreLength+2*depth)+",\"coverage\":"+(Q-hist[INF])+",\"unreachable_count\":"+hist[INF]+",\"maximum_distance\":"+maximum+",\"finite_maximum_distance\":"+finiteMaximum+",\"distance_counts\":"+counts+",\"safe_single_additions\":"+Ints(safe.ToArray())+",\"outside_safe_additions\":"+Ints(outside.ToArray())+",\"five_subset_count\":"+combinations+",\"safe_single_additions_cutoff14\":"+Ints(safe14.ToArray())+"}");
    }
    static int Add(int a,int b){int z=0,p=1;for(int j=0;j<4;j++){z+=((a%5+b%5)%5)*p;a/=5;b/=5;p*=5;}return z;}
    static byte[] Adjoin(byte[] d,int g){byte[] n=(byte[])d.Clone();for(int h=0;h<Q;h++){int k=d[h]+1;if(k<n[plus[g*Q+h]])n[plus[g*Q+h]]=(byte)k;}return n;}
    static bool Safe(byte[] d,int g){return d[neg[g]]>=M&&d[neg[twice[g]]]>=M-1;}
    static byte[] AdjoinBlock(byte[] d,int g){
        byte[] n=(byte[])d.Clone();int a=g*Q,b=twice[g]*Q;
        for(int h=0;h<Q;h++){int k=d[h]+1;if(k<n[plus[a+h]])n[plus[a+h]]=(byte)k;k++;if(k<n[plus[b+h]])n[plus[b+h]]=(byte)k;}
        return n;
    }
    static void Dfs(byte[] d,int[] cand,int count,int depth){
        nodes++;if(nodes>nodeLimit||((nodes&1023)==0&&watch.Elapsed.TotalSeconds>=deadline)){complete=false;return;}
        levels[depth]++;
        if(depth>maxDepth){maxDepth=depth;longest=new int[depth];Array.Copy(path,longest,depth);}
        if(depth==BLOCKS){terminals++;if(firstTerminal==null){firstTerminal=new int[depth];Array.Copy(path,firstTerminal,depth);}Profile(d,depth);return;}
        bool child=false;
        for(int i=0;i<count;i++){
            int g=cand[i];if(!Safe(d,g))throw new Exception("unsafe block");byte[] nd=AdjoinBlock(d,g);
            int[] nc=new int[count-i-1];int nn=0;for(int j=i+1;j<count;j++)if(Safe(nd,cand[j]))nc[nn++]=cand[j];
            path[depth]=g;child=true;Dfs(nd,nc,nn,depth+1);if(!complete)return;
        }
        if(!child)leaves[depth]++;
    }
    static string Ints(int[] a){return a==null?"null":"["+String.Join(",",a)+"]";}
    static string Levels(long[] a){var s=new StringBuilder("{");bool f=true;for(int i=0;i<a.Length;i++)if(a[i]>0){if(!f)s.Append(',');s.Append('"').Append(coreLength+2*i).Append("\":").Append(a[i]);f=false;}return s.Append('}').ToString();}
    static void Line(StreamWriter w,string s){w.WriteLine(s);w.Flush();Console.WriteLine(s);}
    public static void Run(string mode,int cutoff,int target,string filename,int[] skip,int seconds,long limit,string sha){
        bool allDouble=mode=="2222";coreLength=allDouble?8:9;M=cutoff;BLOCKS=(target-coreLength)/2;
        if(target<coreLength||target>22||(target-coreLength)%2!=0)throw new Exception("invalid target");
        nodeLimit=limit;deadline=seconds;
        for(int g=0;g<Q;g++){int x=g;for(int j=0;j<4;j++){digits[g,j]=x%5;x/=5;}twice[g]=Add(g,g);neg[g]=Add(twice[g],twice[g]);for(int h=0;h<Q;h++)plus[g*Q+h]=Add(g,h);}
        byte[] d=new byte[Q];for(int g=1;g<Q;g++)d[g]=INF;var basisSet=new HashSet<int>();
        int[] basis={1,5,25,125};for(int j=0;j<4;j++){basisSet.Add(basis[j]);for(int k=0;k<(!allDouble&&j==0?3:2);k++){if(d[neg[basis[j]]]!=INF)throw new Exception("core zero sum");d=Adjoin(d,basis[j]);}}
        var initial=new List<int>();var roots=new List<int>();
        for(int g=1;g<Q;g++)if(!basisSet.Contains(g)&&Safe(d,g)){initial.Add(g);bool canonical=digits[g,1]>=digits[g,2]&&digits[g,2]>=digits[g,3]&&(!allDouble||digits[g,0]>=digits[g,1]);if(canonical)roots.Add(g);}
        var skipSet=new HashSet<int>(skip);watch=Stopwatch.StartNew();int attempted=0,completed=0,maximum=coreLength;long totalNodes=0,totalTerminal=0;
        using(var w=new StreamWriter(filename,false,new UTF8Encoding(false))){
            evidenceWriter=w;leafProfiles=0;
            Line(w,"{\"type\":\"metadata\",\"group\":\"C_5^4\",\"mode\":\""+mode+"\",\"core_length\":"+coreLength+",\"m\":"+M+",\"target\":"+target+",\"new_blocks\":"+BLOCKS+",\"block_multiplicity\":2,\"initial_safe_count\":"+initial.Count+",\"initial_safe_candidates\":"+Ints(initial.ToArray())+",\"canonical_roots\":"+Ints(roots.ToArray())+",\"script_sha256\":\""+sha+"\"}");
            for(int r=roots.Count-1;r>=0;r--){
                int root=roots[r];if(skipSet.Contains(root))continue;if(watch.Elapsed.TotalSeconds>=deadline)break;
                byte[] d1=AdjoinBlock(d,root);var candidates=new List<int>();foreach(int h in initial)if(h>root&&Safe(d1,h))candidates.Add(h);
                nodes=0;terminals=0;maxDepth=0;complete=true;longest=null;firstTerminal=null;Array.Clear(levels,0,levels.Length);Array.Clear(leaves,0,leaves.Length);
                path[0]=root;double start=watch.Elapsed.TotalSeconds;Dfs(d1,candidates.ToArray(),candidates.Count,1);
                attempted++;if(complete)completed++;totalNodes+=nodes;totalTerminal+=terminals;maximum=Math.Max(maximum,coreLength+2*maxDepth);
                Line(w,"{\"type\":\"root\",\"root\":"+root+",\"completed_exhaustively\":"+(complete?"true":"false")+",\"nodes\":"+nodes+",\"nodes_by_length\":"+Levels(levels)+",\"leaves_by_length\":"+Levels(leaves)+",\"max_reached_length\":"+(coreLength+2*maxDepth)+",\"one_longest_extension_blocks\":"+Ints(longest)+",\"terminal_count\":"+terminals+",\"first_terminal_blocks\":"+Ints(firstTerminal)+",\"seconds\":"+(watch.Elapsed.TotalSeconds-start).ToString("F6",System.Globalization.CultureInfo.InvariantCulture)+"}");
            }
            Line(w,"{\"type\":\"summary\",\"attempted_roots\":"+attempted+",\"completed_roots_this_run\":"+completed+",\"canonical_root_count\":"+roots.Count+",\"all_roots_completed\":"+(completed+skipSet.Count==roots.Count?"true":"false")+",\"nodes_this_run\":"+totalNodes+",\"max_reached_length_this_run\":"+maximum+",\"terminal_count\":"+totalTerminal+",\"leaf_profile_count\":"+leafProfiles+",\"maximum_outside_safe_count\":"+largestOutside+",\"outside_safe_count_distribution\":"+OutsideHistogram()+",\"five_subset_denominator\":"+fiveSubsetDenominator+",\"seconds\":"+watch.Elapsed.TotalSeconds.ToString("F6",System.Globalization.CultureInfo.InvariantCulture)+"}");
        }
    }
}
'@
if (-not $OutputFile) { throw 'OutputFile is required' }
$atomSkip = @()
if ($SkipEvidence) {
    $atomSkip = @(Get-Content -Encoding utf8 -LiteralPath $SkipEvidence | ForEach-Object { $_ | ConvertFrom-Json } | Where-Object { $_.type -eq 'root' -and $_.completed_exhaustively } | ForEach-Object { [int]$_.root })
}
$atomSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $PSCommandPath).Hash.ToLowerInvariant()
Add-Type -TypeDefinition $atomBlockSource -Language CSharp
[Atom3222Length15Scan]::Run($Mode,$Cutoff,$Target,$OutputFile,[int[]]$atomSkip,$Seconds,$NodeLimit,$atomSha)
