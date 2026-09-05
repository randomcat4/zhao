param([string]$OutputFile = '')
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$taskSource = @'
using System;
using System.Collections.Generic;
using System.IO;
using System.Diagnostics;
public static class SearchSupport7Cap3 {
 const int G=625;
 static int[][] plus=new int[G][];
 static int[] neg=new int[G],sum=new int[G];
 static bool[] valid=new bool[G];
 static int Add(int a,int b){int r=0,p=1;for(int i=0;i<4;i++){r+=((a%5+b%5)%5)*p;a/=5;b/=5;p*=5;}return r;}
 static bool IsBasis(int x){return x==1||x==5||x==25||x==125;}
 public static void Run(string output){
  var watch=Stopwatch.StartNew();for(int x=0;x<G;x++){plus[x]=new int[G];neg[x]=Add(Add(x,x),Add(x,x));int z=x;valid[x]=true;for(int i=0;i<4;i++){if(z%5==4)valid[x]=false;sum[x]+=z%5;z/=5;}for(int g=0;g<G;g++)plus[x][g]=Add(x,g);}
  var eligible=new List<int>();for(int x=1;x<G;x++)if(!IsBasis(x))eligible.Add(x);
  StreamWriter writer=null;if(output.Length>0)writer=new StreamWriter(output,false,new System.Text.UTF8Encoding(false));Action<string>log=line=>{Console.WriteLine(line);if(writer!=null){writer.WriteLine(line);writer.Flush();}};
  long pairs=0,surviveA=0,surviveB=0,candidatesA=0,candidatesB=0,badA=0,badB=0;int[] minLen=new int[G];
  for(int ai=0;ai<eligible.Count;ai++)for(int bi=ai+1;bi<eligible.Count;bi++){
   pairs++;int a=eligible[ai],b=eligible[bi];int[]ma=new int[4],mb=new int[4];for(int t=1;t<4;t++){ma[t]=plus[a][ma[t-1]];mb[t]=plus[b][mb[t-1]];}
   int firstZero=100;
   for(int t=0;t<4;t++)for(int u=0;u<4;u++){if(t+u==0)continue;int v=neg[plus[ma[t]][mb[u]]];if(valid[v])firstZero=Math.Min(firstZero,sum[v]+t+u);}
   bool goodA=firstZero>13,goodB=firstZero>14;if(!goodA)continue;surviveA++;if(goodB)surviveB++;
   for(int g=0;g<G;g++)minLen[g]=100;
   for(int t=0;t<4;t++)for(int u=0;u<4;u++){int extra=plus[ma[t]][mb[u]];for(int v=0;v<G;v++)if(valid[v]){int g=plus[extra][v],len=t+u+sum[v];if(len<minLen[g])minLen[g]=len;}}
   foreach(int c in eligible){if(c==a||c==b)continue;int c2=plus[c][c],c3=plus[c][c2];
    if(goodA&&c>b){candidatesA++;if(minLen[neg[c]]>12&&minLen[neg[c2]]>11&&minLen[neg[c3]]>10){badA++;log("BAD A a="+a+" b="+b+" c="+c);}}
    if(goodB){candidatesB++;if(minLen[neg[c]]>13&&minLen[neg[c2]]>12){badB++;log("BAD B a="+a+" b="+b+" c="+c);}}
   }
  }
  log("FINAL pairs="+pairs+" surviveA="+surviveA+" surviveB="+surviveB+" candidatesA="+candidatesA+" candidatesB="+candidatesB+" badA="+badA+" badB="+badB+" ms="+watch.ElapsedMilliseconds);if(writer!=null)writer.Dispose();
 }
}
'@
Add-Type -TypeDefinition $taskSource -Language CSharp
if ($OutputFile) {
    $taskParent = Split-Path -Parent $OutputFile
    if ($taskParent -and -not (Test-Path -LiteralPath $taskParent)) { New-Item -ItemType Directory -Path $taskParent | Out-Null }
}
[SearchSupport7Cap3]::Run($OutputFile)
