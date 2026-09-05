#include <bits/stdc++.h>
using namespace std; constexpr int G=625;using BS=bitset<625>;using Dist=array<uint8_t,G>;
int addg[G][G],ng[G];vector<int> vals,core,path;vector<BS> edges;int need;bool found=false;long long nodes=0,cores=0,cap=0,colors=0;int maxcandidate=0,maxcolor=0;
Dist push(const Dist&d,int g){Dist e=d;for(int h=0;h<G;h++)e[addg[h][g]]=min<int>(e[addg[h][g]],d[h]+1);return e;}
void color(BS P,vector<int>&order,vector<int>&bound){int co=0;while(P.any()){co++;BS Q=P;while(Q.any()){int v=Q._Find_first();P.reset(v);Q.reset(v);Q&=~edges[v];order.push_back(v);bound.push_back(co);}}}
void dfs(BS P,const Dist&d){nodes++;if((int)path.size()==need){cout<<"FOUND";for(int x:core)cout<<" "<<x;for(int x:path)cout<<" "<<x;cout<<endl;found=true;return;}
 for(int v=P._Find_first();v<625;v=P._Find_next(v))if(d[ng[vals[v]]]<13)P.reset(v);
 if(path.size()+P.count()<need)return;vector<int>ord,b;color(P,ord,b);
 for(int i=(int)ord.size()-1;i>=0;i--){if(path.size()+b[i]<need)return;int v=ord[i];if(!P[v])continue;int g=vals[v];auto next=push(d,g);path.push_back(g);dfs(P&edges[v],next);path.pop_back();if(found)return;P.reset(v);}
}
void run_core(const vector<int>&v){Dist d;d.fill(63);d[0]=0;for(int g:v){if(d[ng[g]]<13)return;d=push(d,g);}cores++;core=v;need=21-v.size();vals.clear();
 for(int g=1;g<G;g++)if(find(v.begin(),v.end(),g)==v.end()&&d[ng[g]]>=13)vals.push_back(g);
 int n=vals.size();maxcandidate=max(maxcandidate,n);if(n<need)return;cap++;
 edges.assign(n,BS());for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(d[ng[addg[vals[i]][vals[j]]]]>=12){edges[i].set(j);edges[j].set(i);}
 BS P;for(int i=0;i<n;i++)P.set(i);vector<int>o,b;color(P,o,b);maxcolor=max(maxcolor,b.back());if(b.back()<need)return;colors++;path.clear();dfs(P,d);
}
int main(int argc,char**argv){string mode=argc>1?argv[1]:"a2b3";int lo=argc>2?atoi(argv[2]):1,hi=argc>3?atoi(argv[3]):624;
 for(int x=0;x<G;x++)for(int y=0;y<G;y++){int a=x,b=y,p=1,s=0;for(int j=0;j<4;j++){s+=p*((a%5+b%5)%5);p*=5;a/=5;b/=5;}addg[x][y]=s;}
 for(int x=0;x<G;x++){int a=x,n=0,p=1;for(int j=0;j<4;j++){n+=p*((5-a%5)%5);p*=5;a/=5;}ng[x]=n;}
 vector<int>base={1,1,1,5,5,5,25,25,125,125};
 if(mode=="a2b3"){for(int g=lo;g<=hi;g++)if(g!=1&&g!=5&&g!=25&&g!=125){auto v=base;v.push_back(g);v.push_back(g);run_core(v);if(found)return 0;}}
 else if(mode=="a2b2_rank4")run_core(base);
 else return 3;
 cout<<"COMPLETE mode="<<mode<<" domain="<<lo<<":"<<hi<<" safe_cores="<<cores<<" candidate_pass="<<cap<<" color_pass="<<colors<<" nodes="<<nodes<<" max_candidates="<<maxcandidate<<" max_root_colors="<<maxcolor<<" endpoints="<<found<<endl;
}
