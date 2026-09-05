param(
    [ValidateSet('four','three_double','three_single')][string]$Mode = 'three_double',
    [string]$OutputFile = '',
    [string]$SkipEvidence = '',
    [int]$OnlyRoot = -1,
    [int]$Seconds = 45,
    [long]$NodeLimit = 2000000
)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$atomSource = @'
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;

public static class AtomCoreFast {
    const int Q=625, INF=99, M=13, TARGET=21;
    static readonly int[] basis={1,5,25,125};
    static int[,] digits=new int[Q,4];
    static int[] plus=new int[Q*Q], neg=new int[Q], count=new int[Q], capacity=new int[Q];
    static int[] path=new int[22], longest, firstTerminal;
    static long[] levels=new long[22], leaves=new long[22];
    static long nodes, nodeLimit, terminals;
    static bool complete;
    static int coreLength, maxDepth;
    static Stopwatch watch;
    static double deadline;
    static int Add(int a,int b) { int z=0,p=1;for(int j=0;j<4;j++){z+=((a%5+b%5)%5)*p;a/=5;b/=5;p*=5;}return z; }
    static byte[] Adjoin(byte[] d,int g) {
        byte[] n=(byte[])d.Clone(); int offset=g*Q;
        for(int h=0;h<Q;h++) {int k=d[h]+1;if(k<n[plus[offset+h]])n[plus[offset+h]]=(byte)k;}
        return n;
    }
    static void Dfs(byte[] d,int[] candidates,int number,int depth) {
        nodes++;
        if(nodes>nodeLimit || ((nodes&1023)==0 && watch.Elapsed.TotalSeconds>=deadline)){complete=false;return;}
        levels[coreLength+depth]++;
        if(depth>maxDepth){maxDepth=depth;longest=new int[depth];Array.Copy(path,longest,depth);}
        if(coreLength+depth==TARGET){terminals++;if(firstTerminal==null){firstTerminal=new int[depth];Array.Copy(path,firstTerminal,depth);}return;}
        bool child=false;
        for(int i=0;i<number;i++) {
            int g=candidates[i]; if(count[g]>=capacity[g])continue;
            if(d[neg[g]]<M)throw new Exception("unsafe candidate");
            byte[] nd=Adjoin(d,g); count[g]++;
            int[] following=new int[number-i];int nf=0;
            for(int j=i;j<number;j++){int h=candidates[j];if(count[h]<capacity[h]&&nd[neg[h]]>=M)following[nf++]=h;}
            path[depth]=g;child=true;Dfs(nd,following,nf,depth+1);count[g]--;
            if(!complete)return;
        }
        if(!child)leaves[coreLength+depth]++;
    }
    static string Ints(int[] xs){return xs==null?"null":"["+String.Join(",",xs)+"]";}
    static string Levels(long[] xs){var s=new StringBuilder("{");bool first=true;for(int i=0;i<xs.Length;i++)if(xs[i]>0){if(!first)s.Append(',');s.Append('"').Append(i).Append("\":").Append(xs[i]);first=false;}return s.Append('}').ToString();}
    static void Line(StreamWriter writer,string s){writer.WriteLine(s);writer.Flush();Console.WriteLine(s);}
    public static void Run(string mode,string filename,int[] skip,int onlyRoot,int seconds,long limit,string sha){
        for(int g=0;g<Q;g++){int x=g;for(int j=0;j<4;j++){digits[g,j]=x%5;x/=5;}neg[g]=Add(Add(g,g),Add(g,g));for(int h=0;h<Q;h++)plus[g*Q+h]=Add(g,h);}
        bool four=mode=="four",single=mode=="three_single";
        int last=four?3:(single?1:2);coreLength=9+last;
        for(int g=0;g<Q;g++)capacity[g]=(single&&g>=125)?1:2;
        byte[] initialDist=new byte[Q];for(int g=1;g<Q;g++)initialDist[g]=INF;
        for(int i=0;i<4;i++){int mult=i<3?3:last;capacity[basis[i]]=mult;for(int j=0;j<mult;j++){if(initialDist[neg[basis[i]]]!=INF)throw new Exception("core zero sum");initialDist=Adjoin(initialDist,basis[i]);count[basis[i]]++;}}
        var initial=new List<int>();var roots=new List<int>();
        for(int g=1;g<Q;g++)if(count[g]<capacity[g]&&initialDist[neg[g]]>=M){
            initial.Add(g);bool canonical=true;int length=four?4:3;for(int j=1;j<length;j++)if(digits[g,j-1]<digits[g,j])canonical=false;if(canonical)roots.Add(g);
        }
        var skipSet=new HashSet<int>(skip);
        watch=Stopwatch.StartNew();deadline=seconds;nodeLimit=limit;
        int attempted=0,completed=0;long totalNodes=0,totalTerminal=0;int maximum=coreLength;
        using(var writer=new StreamWriter(filename,false,new UTF8Encoding(false))){
            Line(writer,"{\"type\":\"metadata\",\"mode\":\""+mode+"\",\"m\":13,\"target\":21,\"core_length\":"+coreLength+",\"script_sha256\":\""+sha+"\",\"initial_safe_count\":"+initial.Count+",\"canonical_roots\":"+Ints(roots.ToArray())+",\"skipped_roots\":"+Ints(skip)+"}");
            for(int r=roots.Count-1;r>=0;r--){
                int root=roots[r];if(skipSet.Contains(root)||(onlyRoot>=0&&root!=onlyRoot))continue;
                if(watch.Elapsed.TotalSeconds>=deadline)break;
                nodes=0;terminals=0;maxDepth=0;complete=true;longest=null;firstTerminal=null;Array.Clear(levels,0,levels.Length);Array.Clear(leaves,0,leaves.Length);
                byte[] d1=Adjoin(initialDist,root);count[root]++;var candidates=new List<int>();
                foreach(int h in initial)if(h>=root&&count[h]<capacity[h]&&d1[neg[h]]>=M)candidates.Add(h);
                path[0]=root;double start=watch.Elapsed.TotalSeconds;Dfs(d1,candidates.ToArray(),candidates.Count,1);count[root]--;
                attempted++;if(complete)completed++;totalNodes+=nodes;totalTerminal+=terminals;maximum=Math.Max(maximum,coreLength+maxDepth);
                string row="{\"type\":\"root\",\"root\":"+root+",\"completed_exhaustively\":"+(complete?"true":"false")+",\"nodes\":"+nodes+",\"max_reached_length\":"+(coreLength+maxDepth)+",\"nodes_by_length\":"+Levels(levels)+",\"leaves_by_length\":"+Levels(leaves)+",\"one_longest_extension\":"+Ints(longest)+",\"terminal_count\":"+terminals+",\"first_terminal\":"+Ints(firstTerminal)+",\"seconds\":"+(watch.Elapsed.TotalSeconds-start).ToString("F6",System.Globalization.CultureInfo.InvariantCulture)+"}";
                Line(writer,row);
            }
            Line(writer,"{\"type\":\"summary\",\"attempted_roots\":"+attempted+",\"completed_roots_this_run\":"+completed+",\"canonical_root_count\":"+roots.Count+",\"nodes_this_run\":"+totalNodes+",\"max_reached_length_this_run\":"+maximum+",\"terminal_count\":"+totalTerminal+",\"seconds\":"+watch.Elapsed.TotalSeconds.ToString("F6",System.Globalization.CultureInfo.InvariantCulture)+"}");
        }
    }
}
'@
if (-not $OutputFile) { throw 'OutputFile is required' }
$atomSkip = @()
if ($SkipEvidence) {
    $atomPrevious = Get-Content -Raw -Encoding utf8 -LiteralPath $SkipEvidence | ConvertFrom-Json
    $atomSkip = @($atomPrevious.runs | Where-Object { $_.completed_exhaustively } | ForEach-Object { [int]$_.root })
}
$atomSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $PSCommandPath).Hash.ToLowerInvariant()
Add-Type -TypeDefinition $atomSource -Language CSharp
[AtomCoreFast]::Run($Mode,$OutputFile,[int[]]$atomSkip,$OnlyRoot,$Seconds,$NodeLimit,$atomSha)
