$ErrorActionPreference = 'Stop'
$source = @'
using System;
using System.Collections.Generic;
public static class StructuralSupport6 {
 static List<int[]> Patterns(int total) {
   var list=new List<int[]>();
   for(int a=1;a<=4;a++) for(int b=1;b<=4;b++) for(int c=1;c<=4;c++)
   for(int d=1;d<=4;d++) for(int e=1;e<=4;e++) {
    int f=total-a-b-c-d-e;
    if(f>=1 && f<=4) list.Add(new int[]{a,b,c,d,e,f});
   }
   return list;
 }
 public static string Run() {
   int[][] v=new int[625][];
   for(int a=0;a<625;a++) {v[a]=new int[4]; int z=a; for(int j=0;j<4;j++){v[a][j]=z%5;z/=5;}}
   long matrices=0, checks20=0, checks21=0; int bad20=0,bad21=0;
   var p20=Patterns(20); var p21=Patterns(21);
   var rows=new int[24][];
   for(int a=1;a<625;a++) {
    if(a==1||a==5||a==25||a==125) continue;
    for(int b=a+1;b<625;b++) {
     if(b==1||b==5||b==25||b==125) continue;
     matrices++;
     int ri=0;
     for(int t=0;t<5;t++) for(int u=0;u<5;u++) {
      if(t==0 && u==0) continue;
      int[] r=new int[7]; r[4]=t;r[5]=u;r[6]=t+u;
      for(int j=0;j<4;j++){r[j]=(25-t*v[a][j]-u*v[b][j])%5;if(r[j]<0)r[j]+=5;r[6]+=r[j];}
      rows[ri++]=r;
     }
     for(int pass=0;pass<2;pass++) {
      var patterns=pass==0?p20:p21;int lim=pass==0?14:13;
      foreach(var w in patterns) {
       if(pass==0)checks20++;else checks21++;
       bool ok=false;
       foreach(var r in rows) {
        if(r[6]>lim)continue;
        bool fit=true;for(int j=0;j<6;j++)if(r[j]>w[j]){fit=false;break;}
        if(fit){ok=true;break;}
       }
       if(!ok){if(pass==0)bad20++;else bad21++;Console.WriteLine("BAD "+(pass==0?20:21)+" a="+a+" b="+b+" weights="+string.Join(",",w));}
      }
     }
    }
   }
   return "matrices="+matrices+" patterns20="+p20.Count+" patterns21="+p21.Count+" checks20="+checks20+" checks21="+checks21+" bad20="+bad20+" bad21="+bad21;
 }
}
'@
Add-Type -TypeDefinition $source -Language CSharp
[StructuralSupport6]::Run()
