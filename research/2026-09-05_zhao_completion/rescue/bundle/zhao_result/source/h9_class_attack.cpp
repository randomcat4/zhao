#include <bits/stdc++.h>
using namespace std; using U=uint64_t; using BS=bitset<512>;
struct Mask{U lo,hi; Mask operator&(const Mask&o)const{return {lo&o.lo,hi&o.hi};} Mask& operator&=(const Mask&o){lo&=o.lo;hi&=o.hi;return *this;} bool has(int i)const{return i<64?(lo>>i)&1:(hi>>(i-64))&1;}};
const Mask ALL={~U(0),(U(1)<<61)-1};
int ad[125][125],ng[125],dh[125],add4[625][625];bool good5[125];
Mask allow[10][8][125],ok[10][5]; int M=5,NEED=7; int qchosen[5]={};
long long roots=0,cores=0,dense=0,capacitypass=0,colorpass=0,nodes=0;int maximum_capacity=0;bool found=false;
vector<int> core,verts,chosen;vector<BS> graphv;vector<pair<int,int>> subsetlist;
int add(int a,int b){return add4[a][b];}
bool allowed(int length,int g){return ok[length][g/125].has(g%125);}
void color(BS P,vector<int>&ord,vector<int>&bounds){int co=0;while(P.any()){co++;BS Q=P;while(Q.any()){int v=Q._Find_first();P.reset(v);Q.reset(v);Q&=~graphv[v];ord.push_back(v);bounds.push_back(co);}}}
void dfs(BS P,int hused){nodes++;if(chosen.size()==NEED){found=true;cout<<"FOUND_A";for(int x:core)cout<<" "<<x;for(int i:chosen)cout<<" "<<verts[i];cout<<endl;return;}
 if(chosen.size()+P.count()<NEED)return;vector<int>ord,bounds;color(P,ord,bounds);
 for(int i=(int)ord.size()-1;i>=0;i--){if(chosen.size()+bounds[i]<NEED)return;int v=ord[i];if(!P[v])continue;int g=verts[v];
  bool safe=!(g<125&&hused>=2) && !(g>=125&&qchosen[g/125]>=M);for(auto [s,k]:subsetlist)if(safe&&!allowed(k+1,add(s,g)))safe=false;
  if(safe){int n=subsetlist.size();for(int j=0;j<n;j++)subsetlist.push_back({add(subsetlist[j].first,g),subsetlist[j].second+1});chosen.push_back(v);qchosen[g/125]++;dfs(P&graphv[v],hused+(g<125));chosen.pop_back();qchosen[g/125]--;subsetlist.resize(n);if(found)return;}
  P.reset(v);
 }
}
void process(const vector<int>&R){
 cores++;for(int coordinate=0,p=1;coordinate<3;coordinate++,p*=5){bool eq=true;for(int r:R)if((r/p)%5!=(R[0]/p)%5){eq=false;break;}if(eq&&M>=6){dense++;return;}}
 int sums[128]={},weights[128]={};for(int m=1;m<(1<<M);m++){int j=__builtin_ctz((unsigned)m),old=m&(m-1);sums[m]=ad[sums[old]][R[j]];weights[m]=weights[old]+1;}
 for(int l=1;l<=NEED;l++)for(int q=0;q<5;q++)ok[l][q]=ALL;
 for(int m=0;m<(1<<M);m++){int k=weights[m],q=(5-k%5)%5;for(int l=1;l<=NEED;l++)ok[l][q]&=allow[l][k][sums[m]];}
 verts.clear(); vector<int> hc; int capacity=0;
 for(int u=1;u<125;u++)if(u!=1&&u!=5&&u!=25&&ok[1][0].has(u))hc.push_back(u);
 int hcap=hc.empty()?0:2;
 for(int q: {2,3,4}){int num=0;for(int u=0;u<125;u++)if(ok[1][q].has(u)){verts.push_back(125*q+u);num++;}capacity+=min(num,M);}
 capacity+=hcap;maximum_capacity=max(maximum_capacity,capacity);if(capacity<NEED)return;capacitypass++;
 int n=verts.size();if(n>512){cerr<<"overflow"<<endl;exit(3);}graphv.assign(n,BS());for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(allowed(2,add(verts[i],verts[j]))){graphv[i].set(j);graphv[j].set(i);}
 BS P;for(int i=0;i<n;i++)P.set(i);vector<int>o,b;color(P,o,b);if(b.empty()||b.back()+hcap<NEED)return;
 for(int u:hc){verts.push_back(u);verts.push_back(u);}n=verts.size();if(n>512){cerr<<"overflow"<<endl;exit(3);}graphv.assign(n,BS());for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(allowed(2,add(verts[i],verts[j]))){graphv[i].set(j);graphv[j].set(i);}
 P.reset();for(int i=0;i<n;i++)P.set(i);o.clear();b.clear();color(P,o,b);if(b.empty()||b.back()<NEED)return;colorpass++;
 core={1,1,1,5,5,5,25,25,25};for(int r:R)core.push_back(125+r);chosen.clear();subsetlist={{0,0}};dfs(P,0);
}
int main(int argc,char**argv){int first=argc>1?atoi(argv[1]):1,last=argc>2?atoi(argv[2]):124;M=argc>3?atoi(argv[3]):5;NEED=12-M;if(M<3||M>6)return 3;
 for(int x=0;x<125;x++)for(int y=0;y<125;y++){int a=x,b=y,p=1,s=0;for(int j=0;j<3;j++){s+=p*((a%5+b%5)%5);p*=5;a/=5;b/=5;}ad[x][y]=s;}
 for(int u=0;u<125;u++){int a=u,p=1,n=0,d=0;bool available=true;for(int j=0;j<3;j++){int c=a%5;a/=5;n+=p*((5-c)%5);p*=5;d+=c;if(c==4)available=false;}ng[u]=n;dh[u]=available?d:99;}
 for(int x=0;x<625;x++)for(int y=0;y<625;y++)add4[x][y]=ad[x%125][y%125]+125*((x/125+y/125)%5);
 for(int z=0;z<125;z++)good5[z]=dh[ng[z]]>8;
 for(int l=1;l<=NEED;l++)for(int k=0;k<=7;k++)for(int s=0;s<125;s++){Mask m{0,0};for(int u=0;u<125;u++)if(dh[ng[ad[u][s]]]+k+l>13){if(u<64)m.lo|=U(1)<<u;else m.hi|=U(1)<<(u-64);}allow[l][k][s]=m;}
 for(int a=first;a<=last;a++)for(int b=a+1;b<125;b++){
  if(M==3){roots++;process({0,a,b});if(found)return 0;continue;}
  for(int c=b+1;c<125;c++){
   roots++;if(M==4){process({0,a,b,c});if(found)return 0;continue;}
   array<int,4>R={0,a,b,c};int sum=ad[ad[a][b]][c];vector<int>cand;for(int g=c+1;g<125;g++)if(good5[ad[sum][g]])cand.push_back(g);
   if(M==5){for(int g:cand){process({0,a,b,c,g});if(found)return 0;}continue;}
   bool pairgood[125];for(int z=0;z<125;z++){pairgood[z]=true;for(int omit:R)if(!good5[ad[z][ad[sum][ng[omit]]]]){pairgood[z]=false;break;}}
   for(int i=0;i<(int)cand.size();i++)for(int j=i+1;j<(int)cand.size();j++)if(pairgood[ad[cand[i]][cand[j]]]){process({0,a,b,c,cand[i],cand[j]});if(found)return 0;}
  }
 }
 cout<<"COMPLETE class="<<M<<" interval="<<first<<":"<<last<<" roots="<<roots<<" cores="<<cores<<" dense="<<dense<<" capacity_pass="<<capacitypass<<" color_pass="<<colorpass<<" nodes="<<nodes<<" max_capacity="<<maximum_capacity<<" A_endpoints=0"<<endl;
}
