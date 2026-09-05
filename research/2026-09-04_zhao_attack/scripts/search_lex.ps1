param(
 [int]$N=21,[int]$M=13,[int]$Cap=3,[int]$Seed=15485863,
 [int]$Restarts=200,[int]$Steps=4000,[string]$Mode='full',[string]$OutputFile=''
)
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new()
$taskSource=@'
using System;
using System.Collections.Generic;
using System.IO;
using System.Diagnostics;
public static class SearchLexC54 {
 const int G=625;
 static int[][] minus=new int[G][];
 static int[]neg=new int[G],basis=new int[]{1,5,25,125};
 static int Add(int a,int b){int r=0,p=1;for(int j=0;j<4;j++){r+=(a%5+b%5)%5*p;a/=5;b/=5;p*=5;}return r;}
 static int[][] NewDP(int m){int[][]d=new int[m+1][];for(int k=0;k<=m;k++)d[k]=new int[G];return d;}
 static int[][] Count(int[]s,int m){int[][]d=NewDP(m);d[0][0]=1;int n=0;foreach(int x in s){n++;for(int k=Math.Min(n,m);k>0;k--)for(int g=0;g<G;g++)d[k][g]+=d[k-1][minus[x][g]];}return d;}
 static void Delete(int[][]d,int x,int[][]q,int m){Array.Copy(d[0],q[0],G);for(int k=1;k<=m;k++)for(int g=0;g<G;g++)q[k][g]=d[k][g]-q[k-1][minus[x][g]];}
 static void Insert(int[][]q,int x,int[][]d,int m){Array.Copy(q[0],d[0],G);for(int k=1;k<=m;k++)for(int g=0;g<G;g++)d[k][g]=q[k][g]+q[k-1][minus[x][g]];}
 static int Compare(int[]a,int[]b,int m){for(int k=1;k<=m;k++){if(a[k]<b[k])return -1;if(a[k]>b[k])return 1;}return 0;}
 static int First(int[]a,int m){for(int k=1;k<=m;k++)if(a[k]!=0)return k;return m+1;}
 static int[]Vector(int[][]d,int m){int[]v=new int[m+1];for(int k=1;k<=m;k++)v[k]=d[k][0];return v;}
 static string Spectrum(int[]s){int[][]d=Count(s,s.Length);var list=new List<string>();for(int k=1;k<=s.Length;k++)if(d[k][0]!=0)list.Add(k+":"+d[k][0]);return String.Join(",",list);}
 public static void Run(int n,int m,int cap,int seed,int restarts,int steps,string mode,string output){
  for(int x=0;x<G;x++){neg[x]=Add(Add(x,x),Add(x,x));minus[x]=new int[G];for(int g=0;g<G;g++)minus[x][g]=Add(g,neg[x]);}
  var domain=new List<int>();for(int x=1;x<G;x++){int z=x,sum=0;for(int j=0;j<4;j++){sum+=z%5;z/=5;}if(mode!="affine"||sum%5==1)domain.Add(x);}
  var rng=new Random(seed);var watch=Stopwatch.StartNew();StreamWriter writer=null;if(output.Length>0)writer=new StreamWriter(output,false,new System.Text.UTF8Encoding(false));Action<string>log=line=>{Console.WriteLine(line);if(writer!=null){writer.WriteLine(line);writer.Flush();}};
  log("CONFIG N="+n+" M="+m+" cap="+cap+" seed="+seed+" restarts="+restarts+" steps="+steps+" mode="+mode+" objective=exact_lexicographic_spectrum");
  int[]bestGlobal=null,bestSeq=null;long moves=0,evaluations=0;int[][]v=new int[G][];for(int x=0;x<G;x++)v[x]=new int[m+1];
  for(int run=0;run<restarts;run++){
   int[]s=new int[n],mult=new int[G];for(int j=0;j<4;j++){s[j]=basis[j];mult[s[j]]++;}for(int j=4;j<n;j++){int x;if(run%4==0&&j<4*cap)x=basis[(j-4)%4];else do{x=domain[rng.Next(domain.Count)];}while(mult[x]>=cap);s[j]=x;mult[x]++;}
   int[][]d=Count(s,m),q=NewDP(m);int[]cur=Vector(d,m),bestLocal=(int[])cur.Clone();int stale=0;
   for(int step=0;step<steps;step++){
    if(bestGlobal==null||Compare(cur,bestGlobal,m)<0){bestGlobal=(int[])cur.Clone();bestSeq=(int[])s.Clone();log("BEST min="+First(cur,m)+" support="+new HashSet<int>(s).Count+" run="+run+" step="+step+" moves="+moves+" evaluations="+evaluations+" ms="+watch.ElapsedMilliseconds+" seq="+String.Join(",",s)+" spectrum="+Spectrum(s));if(First(cur,m)>m){log("COUNTEREXAMPLE");if(writer!=null)writer.Dispose();return;}}
    if(Compare(cur,bestLocal,m)<0){bestLocal=(int[])cur.Clone();stale=0;}else stale++;
    if(stale>100&&step%17==0){int changes=1+rng.Next(5);for(int j=0;j<changes;j++){int at=4+rng.Next(n-4),x;mult[s[at]]--;do{x=domain[rng.Next(domain.Count)];}while(mult[x]>=cap);s[at]=x;mult[x]++;}d=Count(s,m);cur=Vector(d,m);bestLocal=(int[])cur.Clone();stale=0;continue;}
    int index=4+rng.Next(n-4),old=s[index];mult[old]--;Delete(d,old,q,m);
    int chosen=-1,ties=0,bestFirst=-1,freeChoice=-1,freeTies=0;
    foreach(int x in domain){if(mult[x]>=cap)continue;for(int k=1;k<=m;k++)v[x][k]=q[k][0]+q[k-1][neg[x]];evaluations++;
     int first=First(v[x],m);if(first>bestFirst){bestFirst=first;freeChoice=x;freeTies=1;}else if(first==bestFirst&&rng.Next(++freeTies)==0)freeChoice=x;
     int cmp=chosen<0?-1:Compare(v[x],v[chosen],m);if(cmp<0){chosen=x;ties=1;}else if(cmp==0&&rng.Next(++ties)==0)chosen=x;
    }
    if(step%250<70&&rng.Next(5)==0)chosen=freeChoice;
    s[index]=chosen;mult[chosen]++;Insert(q,chosen,d,m);cur=(int[])v[chosen].Clone();moves++;
   }
   if((run+1)%20==0)log("PROGRESS runs="+(run+1)+" min="+First(bestGlobal,m)+" moves="+moves+" evaluations="+evaluations+" ms="+watch.ElapsedMilliseconds);
  }
  log("FINAL min="+First(bestGlobal,m)+" moves="+moves+" evaluations="+evaluations+" restarts="+restarts+" steps="+steps+" ms="+watch.ElapsedMilliseconds+" seq="+String.Join(",",bestSeq)+" spectrum="+Spectrum(bestSeq));if(writer!=null)writer.Dispose();
 }
}
'@
Add-Type -TypeDefinition $taskSource -Language CSharp
if($OutputFile){$taskParent=Split-Path -Parent $OutputFile;if($taskParent -and -not(Test-Path -LiteralPath $taskParent)){New-Item -ItemType Directory -Path $taskParent|Out-Null}}
[SearchLexC54]::Run($N,$M,$Cap,$Seed,$Restarts,$Steps,$Mode,$OutputFile)
