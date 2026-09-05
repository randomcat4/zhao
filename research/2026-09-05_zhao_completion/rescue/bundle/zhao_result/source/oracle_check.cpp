#include <bits/stdc++.h>
using namespace std;
int ad[625][625],ng[625];
using D=array<int,625>;
D distance_of(const vector<int>&s){D d;d.fill(99);d[0]=0;for(int x:s){D prev=d;for(int t=0;t<625;t++)d[ad[t][x]]=min(d[ad[t][x]],prev[t]+1);}return d;}
int main(){for(int a=0;a<625;a++)for(int b=0;b<625;b++){int x=a,y=b,k=1,s=0;for(int j=0;j<4;j++){s+=k*((x%5+y%5)%5);k*=5;x/=5;y/=5;}ad[a][b]=s;}
for(int a=0;a<625;a++)for(int b=0;b<625;b++)if(ad[a][b]==0)ng[a]=b;
vector<vector<int>> hs={{1,1,1,5,5,5,25,25,25}};
for(int g=26;g<125;g++){vector<int>h={1,1,1,5,5,5,25,25,g,g};D d;d.fill(99);d[0]=0;bool valid=true;for(int x:h){if(d[ng[x]]<13){valid=false;break;}auto p=d;for(int t=0;t<625;t++)d[ad[t][x]]=min(d[ad[t][x]],p[t]+1);}if(valid)hs.push_back(h);}
mt19937 rng(907031);long long cases=0,comparisons=0;vector<int>pool(124);iota(pool.begin(),pool.end(),1);
for(auto h:hs){D dh=distance_of(h);for(int m=3;m<=6;m++)for(int trial=0;trial<12;trial++){
 shuffle(pool.begin(),pool.end(),rng);vector<int> r={0};for(int j=0;j<m-1;j++)r.push_back(pool[j]);vector<int>core=h;for(int u:r)core.push_back(125+u);D dc=distance_of(core);
 int sum[128]={},wt[128]={};for(int mask=1;mask<(1<<m);mask++){int j=__builtin_ctz((unsigned)mask),p=mask&(mask-1);sum[mask]=ad[sum[p]][r[j]];wt[mask]=wt[p]+1;}
 for(int l=1;l<=9;l++)for(int g=0;g<625;g++){
  bool safe=true;for(int mask=0;mask<(1<<m);mask++)if((g/125+wt[mask])%5==0){int s=ad[g%125][sum[mask]],n=ng[s];if(dh[n]+wt[mask]+l<=13){safe=false;break;}}
  bool direct=dc[ng[g]]+l>13;comparisons++;if(safe!=direct){cerr<<"MISMATCH"<<endl;return 2;}
 }
 cases++;
}}
cout<<"PASS H_core_types="<<hs.size()<<" full_cores="<<cases<<" exact_length_queries="<<comparisons<<" mismatches=0"<<endl;
}
