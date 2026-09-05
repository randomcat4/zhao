#include <array>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
using B=uint64_t;
int plus3[125][125],minus3[125][125],minuspoint[125];bool ok5[125];
int mind[125];long long roots=0,sevens=0;int maxcap=0,maxsame=0;int coreg=0;long long hist[626]={};
void verify_seven(const array<int,7>&R){
 sevens++; int sums[128]={},wt[128]={};
 for(int mask=1;mask<128;mask++){int j=__builtin_ctz((unsigned)mask),old=mask&(mask-1);sums[mask]=plus3[sums[old]][R[j]];wt[mask]=wt[old]+1;}
 int cap=0,same=0;
 for(int q=0;q<5;q++)for(int u=0;u<125;u++){
  bool safe=true;
  for(int mask=0;mask<128;mask++)if((q+wt[mask])%5==0){int z=minuspoint[plus3[u][sums[mask]]];if(mind[z]+wt[mask]+1<=13){safe=false;break;}}
  if(!safe)continue;
  if(q==1)same++;
  if(q==0){if(u==1||u==5||u==25||u==coreg||u==0)continue;cap+=1;}
  else {bool existing=q==1&&find(R.begin(),R.end(),u)!=R.end();if(!existing)cap++;}
 }
 hist[cap]++;maxcap=max(maxcap,cap);maxsame=max(maxsame,same);
 if(false){cerr<<"DISAGREEMENT cap="<<cap<<" same="<<same<<" R";for(int v:R)cerr<<" "<<v;cerr<<endl;exit(2);}
}
int main(int argc,char**argv){coreg=argc>1?atoi(argv[1]):26;
 for(int x=0;x<125;x++)for(int y=0;y<125;y++){int a=x,b=y,k=1,s=0,d=0;for(int i=0;i<3;i++){s+=k*((a%5+b%5)%5);d+=k*((a%5-b%5+5)%5);a/=5;b/=5;k*=5;}plus3[x][y]=s;minus3[x][y]=d;}
 for(int x=0;x<125;x++){minuspoint[x]=minus3[0][x];int a=x,c=0;bool avail=true;for(int i=0;i<3;i++){int t=a%5;a/=5;if(t==4)avail=false;c+=t;}mind[x]=avail?c:99;}
 array<int,125> distance;distance.fill(99);distance[0]=0;
 for(int g:vector<int>{1,1,1,5,5,5,25,25,coreg,coreg}){if(distance[minuspoint[g]]<13)return 4;auto previous=distance;for(int t=0;t<125;t++)distance[plus3[t][g]]=min(distance[plus3[t][g]],previous[t]+1);}
 for(int t=0;t<125;t++)mind[t]=distance[t];
 for(int z=0;z<125;z++)ok5[z]=mind[minuspoint[z]]>8;
 for(int a=1;a<125;a++)for(int b=a+1;b<125;b++)for(int c=b+1;c<125;c++){
  roots++;array<int,4>root={0,a,b,c};int t=plus3[plus3[a][b]][c];vector<int> cand;
  for(int g=c+1;g<125;g++)if(ok5[plus3[t][g]])cand.push_back(g);
  if(cand.size()<3)continue;if(cand.size()>64)return 3;
  B neighbors[64]={};bool pair_ok[125];
  for(int v=0;v<125;v++){pair_ok[v]=true;for(int omitted:root)if(!ok5[plus3[v][minus3[t][omitted]]]){pair_ok[v]=false;break;}}
  int n=cand.size();for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(pair_ok[plus3[cand[i]][cand[j]]])neighbors[i]|=B(1)<<j;
  for(int i=0;i<n;i++){B J=neighbors[i];while(J){int j=__builtin_ctzll(J);J&=J-1;B K=neighbors[i]&neighbors[j];while(K){int k=__builtin_ctzll(K);K&=K-1;int z=plus3[plus3[cand[i]][cand[j]]][cand[k]];bool valid=true;
    for(int u=0;u<4&&valid;u++)for(int v=u+1;v<4;v++)if(!ok5[plus3[z][plus3[root[u]][root[v]]]]){valid=false;break;}
    if(valid)verify_seven({0,a,b,c,cand[i],cand[j],cand[k]});
  }}}
 }
 cout<<"H10 g="<<coreg<<" COMPLETE roots="<<roots<<" normalized_sevens="<<sevens<<" max_extension_capacity="<<maxcap<<" max_same_coset_extensions="<<maxsame<<" cap_hist=";
 for(int i=0;i<626;i++)if(hist[i])cout<<i<<":"<<hist[i]<<",";cout<<endl;
}
