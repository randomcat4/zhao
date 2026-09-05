param(
    [string]$CoreFile = '',
    [string]$OutputFile = '',
    [string]$SkipEvidence = '',
    [int]$Cutoff = 13,
    [int]$Target = 21,
    [int]$Seconds = 45,
    [long]$NodeLimit = 2000000
)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$atomHSource = @'
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;
public static class AtomHOutside {
    const int Q=625, INF=99;
    static int[] plus=new int[Q*Q], neg=new int[Q], path=new int[22], longest, firstTerminal;
    static long[] levels=new long[22], leaves=new long[22];
    static long nodes,nodeLimit,terminals;
    static int m,target,coreLength,maxDepth;
    static bool complete;
    static Stopwatch watch;
    static double deadline;
    static int Add(int a,int b){int z=0,p=1;for(int j=0;j<4;j++){z+=((a%5+b%5)%5)*p;a/=5;b/=5;p*=5;}return z;}
    static byte[] Adjoin(byte[] d,int g){byte[] n=(byte[])d.Clone();for(int h=0;h<Q;h++){int k=d[h]+1;if(k<n[plus[g*Q+h]])n[plus[g*Q+h]]=(byte)k;}return n;}
    static void Dfs(byte[] d,int[] cand,int count,int depth){
        nodes++;if(nodes>nodeLimit || ((nodes&1023)==0 && watch.Elapsed.TotalSeconds>=deadline)){complete=false;return;}
        levels[coreLength+depth]++;
        if(depth>maxDepth){maxDepth=depth;longest=new int[depth];Array.Copy(path,longest,depth);}
        if(coreLength+depth==target){terminals++;if(firstTerminal==null){firstTerminal=new int[depth];Array.Copy(path,firstTerminal,depth);}return;}
        bool child=false;
        for(int i=0;i<count;i++){
            int g=cand[i];if(d[neg[g]]<m)throw new Exception("unsafe candidate");
            byte[] nd=Adjoin(d,g);int[] nc=new int[count-i-1];int nn=0;
            for(int j=i+1;j<count;j++){int h=cand[j];if(nd[neg[h]]>=m)nc[nn++]=h;}
            path[depth]=g;child=true;Dfs(nd,nc,nn,depth+1);if(!complete)return;
        }
        if(!child)leaves[coreLength+depth]++;
    }
    static string Ints(int[] a){return a==null?"null":"["+String.Join(",",a)+"]";}
    static string Levels(long[] a){var s=new StringBuilder("{");bool f=true;for(int i=0;i<a.Length;i++)if(a[i]>0){if(!f)s.Append(',');s.Append('"').Append(i).Append("\":").Append(a[i]);f=false;}return s.Append('}').ToString();}
    static void Line(StreamWriter w,string s){w.WriteLine(s);w.Flush();Console.WriteLine(s);}
    public static void Run(string specification,string filename,string[] skip,int cutoff,int endpoint,int seconds,long limit,string sha,string inputSha){
        m=cutoff;target=endpoint;nodeLimit=limit;deadline=seconds;
        for(int g=0;g<Q;g++){neg[g]=Add(Add(g,g),Add(g,g));for(int h=0;h<Q;h++)plus[g*Q+h]=Add(g,h);}
        string[] specs=specification.Split(';');var skipSet=new HashSet<string>(skip);
        watch=Stopwatch.StartNew();int attempted=0,completed=0,maximum=0;long totalNodes=0,totalTerminal=0;
        using(var w=new StreamWriter(filename,false,new UTF8Encoding(false))){
            Line(w,"{\"type\":\"metadata\",\"m\":"+m+",\"target\":"+target+",\"canonical_core_count\":"+specs.Length+",\"script_sha256\":\""+sha+"\",\"core_file_sha256\":\""+inputSha+"\",\"outside_capacity\":1,\"fixed_outside_element\":125}");
            for(int r=specs.Length-1;r>=0;r--){
                string spec=specs[r];if(skipSet.Contains(spec))continue;if(watch.Elapsed.TotalSeconds>=deadline)break;
                var hAdded=new List<int>();if(spec.Length>0)foreach(string s in spec.Split(','))hAdded.Add(Int32.Parse(s));
                byte[] d=new byte[Q];for(int g=1;g<Q;g++)d[g]=INF;
                foreach(int b in new int[]{1,5,25})for(int i=0;i<3;i++){if(d[neg[b]]!=INF)throw new Exception("core zero sum");d=Adjoin(d,b);}
                foreach(int g in hAdded){if(g<=0||g>=125||d[neg[g]]!=INF)throw new Exception("bad H core");d=Adjoin(d,g);}
                d=Adjoin(d,125);coreLength=10+hAdded.Count;
                var candidates=new List<int>();for(int g=126;g<Q;g++)if(d[neg[g]]>=m)candidates.Add(g);
                nodes=0;terminals=0;maxDepth=0;complete=true;longest=new int[0];firstTerminal=null;Array.Clear(levels,0,levels.Length);Array.Clear(leaves,0,leaves.Length);
                double start=watch.Elapsed.TotalSeconds;Dfs(d,candidates.ToArray(),candidates.Count,0);
                attempted++;if(complete)completed++;totalNodes+=nodes;totalTerminal+=terminals;maximum=Math.Max(maximum,coreLength+maxDepth);
                Line(w,"{\"type\":\"core\",\"core_id\":\""+spec+"\",\"h_added\":"+Ints(hAdded.ToArray())+",\"core_length\":"+coreLength+",\"initial_safe_count\":"+candidates.Count+",\"completed_exhaustively\":"+(complete?"true":"false")+",\"nodes\":"+nodes+",\"nodes_by_length\":"+Levels(levels)+",\"leaves_by_length\":"+Levels(leaves)+",\"max_reached_length\":"+(coreLength+maxDepth)+",\"one_longest_extension\":"+Ints(longest)+",\"terminal_count\":"+terminals+",\"first_terminal\":"+Ints(firstTerminal)+",\"seconds\":"+(watch.Elapsed.TotalSeconds-start).ToString("F6",System.Globalization.CultureInfo.InvariantCulture)+"}");
            }
            Line(w,"{\"type\":\"summary\",\"attempted_cores\":"+attempted+",\"completed_cores_this_run\":"+completed+",\"canonical_core_count\":"+specs.Length+",\"nodes_this_run\":"+totalNodes+",\"max_reached_length_this_run\":"+maximum+",\"terminal_count\":"+totalTerminal+",\"seconds\":"+watch.Elapsed.TotalSeconds.ToString("F6",System.Globalization.CultureInfo.InvariantCulture)+"}");
        }
    }
}
'@
if (-not $CoreFile -or -not $OutputFile) { throw 'CoreFile and OutputFile are required' }
$atomCores = Get-Content -Raw -Encoding utf8 -LiteralPath $CoreFile | ConvertFrom-Json
if (-not $atomCores.completed_exhaustively) { throw 'H core preparation was incomplete' }
$atomSpecs = @($atomCores.cores | ForEach-Object { $_.added -join ',' }) -join ';'
$atomSkip = @()
if ($SkipEvidence) {
    $atomSkip = @(Get-Content -Encoding utf8 -LiteralPath $SkipEvidence | ForEach-Object { $_ | ConvertFrom-Json } | Where-Object { $_.type -eq 'core' -and $_.completed_exhaustively } | ForEach-Object { [string]$_.core_id })
}
$atomSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $PSCommandPath).Hash.ToLowerInvariant()
$atomInputSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $CoreFile).Hash.ToLowerInvariant()
Add-Type -TypeDefinition $atomHSource -Language CSharp
[AtomHOutside]::Run($atomSpecs,$OutputFile,[string[]]$atomSkip,$Cutoff,$Target,$Seconds,$NodeLimit,$atomSha,$atomInputSha)
