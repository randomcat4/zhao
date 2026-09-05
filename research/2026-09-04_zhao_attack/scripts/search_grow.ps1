param(
 [int]$N=20,[int]$M=14,[int]$Cap=3,[int]$Seed=32452843,[int]$Iterations=100000,
 [string]$Mode='full',[string]$OutputFile=''
)
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new()
$taskSource=@'
using System;
using System.Collections.Generic;
using System.IO;
using System.Diagnostics;
public static class SearchGrowC54 {
 const int G=625,INF=100;
 static int[][] minus=new int[G][];
 static int[] neg=new int[G];
 static int Add(int a,int b){int r=0,p=1;for(int j=0;j<4;j++){r+=(a%5+b%5)%5*p;a/=5;b/=5;p*=5;}return r;}
 static void Rebuild(List<int>s,int[]d,int[]scratch){for(int g=0;g<G;g++)d[g]=INF;d[0]=0;foreach(int x in s){for(int g=0;g<G;g++)scratch[g]=Math.Min(d[g],d[minus[x][g]]+1);Array.Copy(scratch,d,G);}}
 static string Spectrum(List<int>s){long[][]d=new long[s.Count+1][];for(int k=0;k<=s.Count;k++)d[k]=new long[G];d[0][0]=1;int n=0;foreach(int x in s){n++;for(int k=n;k>0;k--)for(int g=0;g<G;g++)d[k][g]+=d[k-1][minus[x][g]];}var a=new List<string>();for(int k=1;k<=n;k++)if(d[k][0]>0)a.Add(k+":"+d[k][0]);return String.Join(",",a);}
 public static void Run(int target,int m,int cap,int seed,int iterations,string mode,string output){
  for(int x=0;x<G;x++){neg[x]=Add(Add(x,x),Add(x,x));minus[x]=new int[G];for(int g=0;g<G;g++)minus[x][g]=Add(g,neg[x]);}
  var domain=new List<int>();for(int x=1;x<G;x++){int z=x,sum=0;for(int j=0;j<4;j++){sum+=z%5;z/=5;}if(mode!="affine"||sum%5==1)domain.Add(x);}
  var rng=new Random(seed);var watch=Stopwatch.StartNew();StreamWriter writer=null;if(output.Length>0)writer=new StreamWriter(output,false,new System.Text.UTF8Encoding(false));Action<string>log=line=>{Console.WriteLine(line);if(writer!=null){writer.WriteLine(line);writer.Flush();}};
  log("CONFIG N="+target+" M="+m+" cap="+cap+" seed="+seed+" iterations="+iterations+" mode="+mode);
  int best=0;List<int> bestSeq=null;long choices=0,extensions=0;int[]mult=new int[G],d=new int[G],scratch=new int[G];var s=new List<int>();int[]basis=new int[]{1,5,25,125};
  for(int iter=0;iter<iterations;iter++){
   if(iter%500==0){s.Clear();Array.Clear(mult,0,G);foreach(int x in basis){s.Add(x);mult[x]++;}Rebuild(s,d,scratch);}
   var possible=new List<int>();foreach(int x in domain)if(mult[x]<cap&&d[neg[x]]>=m)possible.Add(x);choices+=domain.Count;
   if(possible.Count>0){
    int chosen=possible[rng.Next(possible.Count)];
    if(rng.Next(3)!=0&&possible.Count>1){double bestScore=Double.NegativeInfinity;int samples=Math.Min(possible.Count,30);for(int j=0;j<samples;j++){int x=possible[rng.Next(possible.Count)];double score=0;foreach(int y in domain)if(mult[y]<cap&&d[neg[y]]>=m&&d[minus[x][neg[y]]]+1>=m)score++;score+=rng.NextDouble()*Math.Max(1,0.1*possible.Count);if(score>bestScore){bestScore=score;chosen=x;}}}
    s.Add(chosen);mult[chosen]++;for(int g=0;g<G;g++)scratch[g]=Math.Min(d[g],d[minus[chosen][g]]+1);Array.Copy(scratch,d,G);extensions++;
    if(s.Count>best){best=s.Count;bestSeq=new List<int>(s);log("BEST length="+best+" iter="+iter+" choices="+choices+" extensions="+extensions+" ms="+watch.ElapsedMilliseconds+" seq="+String.Join(",",s)+" spectrum="+Spectrum(s));if(best>=target){log("COUNTEREXAMPLE");if(writer!=null)writer.Dispose();return;}}
   }else{
    int remove=Math.Min(s.Count-4,1+rng.Next(5));for(int j=0;j<remove;j++){int at=4+rng.Next(s.Count-4);mult[s[at]]--;s.RemoveAt(at);}Rebuild(s,d,scratch);
   }
  }
  log("FINAL length="+best+" choices="+choices+" extensions="+extensions+" iterations="+iterations+" ms="+watch.ElapsedMilliseconds+" seq="+String.Join(",",bestSeq)+" spectrum="+Spectrum(bestSeq));if(writer!=null)writer.Dispose();
 }
}
'@
Add-Type -TypeDefinition $taskSource -Language CSharp
if($OutputFile){$taskParent=Split-Path -Parent $OutputFile;if($taskParent -and -not(Test-Path -LiteralPath $taskParent)){New-Item -ItemType Directory -Path $taskParent|Out-Null}}
[SearchGrowC54]::Run($N,$M,$Cap,$Seed,$Iterations,$Mode,$OutputFile)
