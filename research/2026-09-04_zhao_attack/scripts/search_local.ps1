param(
    [int]$N = 20,
    [int]$M = 14,
    [int]$Seed = 104729,
    [int]$Restarts = 100,
    [int]$Steps = 4000,
    [double]$Weight = 1.0,
    [int]$Cap = 4,
    [string]$Mode = 'full',
    [string]$OutputFile = ''
)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$taskSource = @'
using System;
using System.Collections.Generic;
using System.IO;
using System.Diagnostics;
public static class SearchLocalC54 {
 const int G=625;
 static int[][] plus = new int[G][], minus = new int[G][];
 static int[] neg = new int[G];
 static int[] basis = new int[]{1,5,25,125};
 static int Add(int a,int b) { int p=1,r=0; for(int i=0;i<4;i++){r+=((a%5+b%5)%5)*p;a/=5;b/=5;p*=5;}return r; }
 static void Init(){for(int x=0;x<G;x++){neg[x]=Add(Add(x,x),Add(x,x));plus[x]=new int[G];minus[x]=new int[G];for(int g=0;g<G;g++)plus[x][g]=Add(x,g);}for(int x=0;x<G;x++)for(int g=0;g<G;g++)minus[x][g]=plus[neg[x]][g];}
 static int[][] NewDP(int m){int[][] d=new int[m+1][];for(int k=0;k<=m;k++)d[k]=new int[G];return d;}
 static int[][] Count(int[] s,int m){int[][]d=NewDP(m);d[0][0]=1;int len=0;foreach(int x in s){len++;for(int k=Math.Min(len,m);k>=1;k--){int[]prev=d[k-1],cur=d[k],trans=plus[x];for(int g=0;g<G;g++)cur[trans[g]]+=prev[g];}}return d;}
 static void Delete(int[][] d,int x,int[][] q,int m){Array.Copy(d[0],q[0],G);int[]trans=minus[x];for(int k=1;k<=m;k++){int[]cur=q[k],prev=q[k-1],orig=d[k];for(int g=0;g<G;g++)cur[g]=orig[g]-prev[trans[g]];}}
 static void Insert(int[][]q,int y,int[][]d,int m){Array.Copy(q[0],d[0],G);int[]trans=minus[y];for(int k=1;k<=m;k++){int[]cur=d[k],same=q[k],prev=q[k-1];for(int g=0;g<G;g++)cur[g]=same[g]+prev[trans[g]];}}
 static int Bad(int[][]d,int m){int n=0;for(int k=1;k<=m;k++)n+=d[k][0];return n;}
 static double WeightedBad(int[][]d,int m,double[]w){double n=0;for(int k=1;k<=m;k++)n+=w[k]*d[k][0];return n;}
 static string Seq(int[]s){return String.Join(",",s);}
 static string Spectrum(int[]s){int[][]d=Count(s,s.Length);var r=new List<string>();for(int k=1;k<=s.Length;k++)if(d[k][0]>0)r.Add(k+":"+d[k][0]);return String.Join(",",r);}
 static int Support(int[]s){return new HashSet<int>(s).Count;}
 public static void Run(int n,int m,int seed,int restarts,int steps,double weight,int cap,string mode,string output){
  Init(); var rng=new Random(seed); var watch=Stopwatch.StartNew(); long moves=0,evaluations=0; double globalBest=Double.PositiveInfinity; int[]globalSeq=null;double[]w=new double[m+1];double binom=1;for(int k=1;k<=m;k++){binom=binom*(n-k+1)/k;w[k]=weight>0?Math.Pow(weight,m-k):100000.0/binom;}
  StreamWriter writer=null;if(output.Length>0)writer=new StreamWriter(output,false,new System.Text.UTF8Encoding(false));
  Action<string> log=(line)=>{Console.WriteLine(line);if(writer!=null){writer.WriteLine(line);writer.Flush();}};
  int[] domain;
  if(mode=="affine"){var list=new List<int>();for(int x=1;x<G;x++){int z=x,sum=0;for(int j=0;j<4;j++){sum+=z%5;z/=5;}if(sum%5==1)list.Add(x);}domain=list.ToArray();}
  else {domain=new int[624];for(int i=0;i<624;i++)domain[i]=i+1;}
  log("CONFIG N="+n+" M="+m+" seed="+seed+" restarts="+restarts+" steps="+steps+" weight="+weight+" cap="+cap+" mode="+mode+" domain="+domain.Length);
  for(int run=0;run<restarts;run++){
   int[]s=new int[n],multiplicity=new int[G];for(int j=0;j<4;j++){s[j]=basis[j];multiplicity[s[j]]++;}
   for(int j=4;j<n;j++){int x;if(run%4==0&&j<4*cap)x=basis[(j-4)%4];else {do{x=domain[rng.Next(domain.Length)];}while(multiplicity[x]>=cap);}s[j]=x;multiplicity[x]++;}
   int[][]d=Count(s,m),q=NewDP(m);double current=WeightedBad(d,m,w),localBest=current;int stale=0;double[]scores=new double[G];
   for(int step=0;step<steps;step++){
    if(current<globalBest){globalBest=current;globalSeq=(int[])s.Clone();log("BEST score="+globalBest.ToString("R")+" bad="+Bad(d,m)+" support="+Support(s)+" run="+run+" step="+step+" moves="+moves+" evaluations="+evaluations+" ms="+watch.ElapsedMilliseconds+" seq="+Seq(s)+" spectrum="+Spectrum(s));if(Bad(d,m)==0){log("COUNTEREXAMPLE");if(writer!=null)writer.Dispose();return;}}
    if(current<localBest){localBest=current;stale=0;}else stale++;
    if(stale>80&&step%13==0){int changes=1+rng.Next(5);for(int j=0;j<changes;j++){int idx=4+rng.Next(n-4),old=s[idx],next; multiplicity[old]--;do{next=domain[rng.Next(domain.Length)];}while(multiplicity[next]>=cap);s[idx]=next;multiplicity[next]++;}d=Count(s,m);current=WeightedBad(d,m,w);stale=0;localBest=current;continue;}
    int at=4+rng.Next(n-4),xold=s[at];multiplicity[xold]--;Delete(d,xold,q,m);double constant=WeightedBad(q,m,w);
    foreach(int y in domain){if(multiplicity[y]>=cap){scores[y]=Double.PositiveInfinity;continue;}double v=constant;for(int k=0;k<m;k++)v+=w[k+1]*q[k][neg[y]];scores[y]=v;evaluations++;}
    int chosen=xold;double t=(step%300<80)?0.14:0.018;double bestNoisy=Double.PositiveInfinity;
    foreach(int y in domain){if(Double.IsPositiveInfinity(scores[y]))continue;double noise=-Math.Log(Math.Max(1e-12,rng.NextDouble()));double value=Math.Log(1.0+scores[y])+t*noise;if(value<bestNoisy){bestNoisy=value;chosen=y;}}
    s[at]=chosen;multiplicity[chosen]++;Insert(q,chosen,d,m);current=scores[chosen];moves++;
   }
   if((run+1)%10==0)log("PROGRESS runs="+(run+1)+" best="+globalBest+" moves="+moves+" evaluations="+evaluations+" ms="+watch.ElapsedMilliseconds);
  }
  log("FINAL score="+globalBest.ToString("R")+" bad="+Bad(Count(globalSeq,m),m)+" moves="+moves+" evaluations="+evaluations+" restarts="+restarts+" steps="+steps+" ms="+watch.ElapsedMilliseconds+" seq="+Seq(globalSeq)+" spectrum="+Spectrum(globalSeq));
  if(writer!=null)writer.Dispose();
 }
}
'@
Add-Type -TypeDefinition $taskSource -Language CSharp
if ($OutputFile) {
    $taskParent = Split-Path -Parent $OutputFile
    if ($taskParent -and -not (Test-Path -LiteralPath $taskParent)) { New-Item -ItemType Directory -Path $taskParent | Out-Null }
}
[SearchLocalC54]::Run($N,$M,$Seed,$Restarts,$Steps,$Weight,$Cap,$Mode,$OutputFile)
