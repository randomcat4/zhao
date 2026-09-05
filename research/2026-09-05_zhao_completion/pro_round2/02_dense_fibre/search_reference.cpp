// Exact extension search conditional on separately proved normalization lemmas.
// No node/pool/time cutoff. Integer arithmetic only. Searches all input roots.
#include <array>
#include <vector>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdint>
#include <climits>
#include <chrono>
#include <stdexcept>
using namespace std;
constexpr int Q=625,F=156,W=8;
static uint16_t ad[Q][Q],negv[Q],mul[5][Q],dir[Q];
struct B156{uint64_t a[3]={};};
static B156 hm[Q];static vector<int>hs[Q];static bool member[Q];static vector<int>S;static int cap;
static uint64_t nodes,prune_size,prune_color;static int maximum;
using Dist=array<uint8_t,Q>;using HC=array<uint8_t,F>;
struct B512{uint64_t a[W]={};void set(int v){a[v>>6]|=uint64_t(1)<<(v&63);}void reset(int v){a[v>>6]&=~(uint64_t(1)<<(v&63));}bool test(int v)const{return(a[v>>6]>>(v&63))&1;}int first()const{for(int i=0;i<W;i++)if(a[i])return 64*i+__builtin_ctzll(a[i]);return -1;}void exclude(B512 const&b){for(int i=0;i<W;i++)a[i]&=~b.a[i];}};
array<int,4>dec(int x){array<int,4>a;for(int j=3;j>=0;j--){a[j]=x%5;x/=5;}return a;}
int enc(array<int,4>a){int x=0;for(int v:a)x=5*x+v;return x;}
void init(){for(int x=0;x<Q;x++){auto a=dec(x);for(int c=0;c<5;c++){auto b=a;for(int&v:b)v=v*c%5;mul[c][x]=enc(b);}negv[x]=mul[4][x];int t=0;for(int v:a)if(v){t=v;break;}if(t){int c=1;while(c*t%5!=1)c++;dir[x]=mul[c][x];}for(int y=0;y<Q;y++){auto b=dec(y);for(int j=0;j<4;j++)b[j]=(a[j]+b[j])%5;ad[x][y]=enc(b);}}
vector<int>fun;for(int x=1;x<Q;x++)if(dir[x]==x)fun.push_back(x);if(fun.size()!=F)throw runtime_error("functional count");for(int x=1;x<Q;x++){auto a=dec(x);for(int k=0;k<F;k++){auto b=dec(fun[k]);int t=0;for(int j=0;j<4;j++)t+=a[j]*b[j];if(t%5==0){hm[x].a[k>>6]|=uint64_t(1)<<(k&63);hs[x].push_back(k);}}if(hs[x].size()!=31)throw runtime_error("hyperplane degree");}}
void bump(uint64_t&n){if(n==UINT64_MAX)throw overflow_error("counter overflow");n++;}
bool geometric_pair(int x,int y,B156 const&nearly){if(dir[x]==dir[y])return false;int t=ad[x][y];if(member[mul[2][t]]||member[mul[3][t]])return false;if(member[ad[mul[2][x]][negv[y]]]||member[ad[mul[3][x]][negv[y]]]||member[ad[mul[2][y]][negv[x]]]||member[ad[mul[3][y]][negv[x]]])return false;for(int k=0;k<3;k++)if(hm[x].a[k]&hm[y].a[k]&nearly.a[k])return false;return true;}
bool one_ok(int x,Dist const&d,HC const&hc){if(member[x]||d[negv[x]]<=12)return false;for(int k:hs[x])if(hc[k]>=cap)return false;for(int y:S){if(dir[x]==dir[y])return false;int t=ad[x][y];if(member[mul[2][t]]||member[mul[3][t]]||member[ad[mul[2][x]][negv[y]]]||member[ad[mul[3][x]][negv[y]]])return false;}return true;}
Dist extend(Dist const&d,int x){Dist e;for(int g=0;g<Q;g++)e[g]=min<int>(d[g],min<int>(14,1+d[ad[g][negv[x]]]));return e;}
bool dfs(vector<int>const&cand,Dist const&d,HC const&hc){bump(nodes);maximum=max(maximum,(int)S.size());if(S.size()==21){cout<<"CANDIDATE_FOUND";for(int v:S)cout<<' '<<v;cout<<'\n';cout.flush();return true;}if(S.size()+cand.size()<21){bump(prune_size);return false;}int n=cand.size();if(n>512)throw runtime_error("bitset capacity");B156 nearly;for(int k=0;k<F;k++)if(hc[k]==cap-1)nearly.a[k>>6]|=uint64_t(1)<<(k&63);
vector<B512>adj(n);for(int i=0;i<n;i++)for(int j=0;j<i;j++){int x=cand[i],y=cand[j];if(d[negv[ad[x][y]]]>11&&geometric_pair(x,y,nearly)){adj[i].set(j);adj[j].set(i);}}
B512 uncolored;for(int i=0;i<n;i++)uncolored.set(i);vector<int>order,bound;int c=0;while(uncolored.first()!=-1){c++;B512 available=uncolored;int v;while((v=available.first())!=-1){order.push_back(v);bound.push_back(c);uncolored.reset(v);available.reset(v);available.exclude(adj[v]);}}
for(int i=n-1;i>=0;i--){if(S.size()+bound[i]<21){bump(prune_color);return false;}int vi=order[i],v=cand[vi];auto nd=extend(d,v);HC nh=hc;for(int k:hs[v])nh[k]++;member[v]=true;S.push_back(v);vector<int>next;for(int j=0;j<i;j++){int ui=order[j];if(adj[vi].test(ui)&&one_ok(cand[ui],nd,nh))next.push_back(cand[ui]);}bool found=false;if(S.size()+next.size()>=21)found=dfs(next,nd,nh);else bump(prune_size);S.pop_back();member[v]=false;if(found)return true;}return false;}
int main(int argc,char**argv){try{if(argc!=2)throw runtime_error("usage extension_search rootfile");init();ifstream f(argv[1]);if(!f)throw runtime_error("root file");vector<vector<int>>roots;string line;while(getline(f,line)){istringstream ss(line);int n,v;ss>>n;vector<int>a;while(ss>>v)a.push_back(v);if((n<7||n>9)||(int)a.size()!=n)throw runtime_error("bad root");roots.push_back(a);}if(roots.size()!=1786)throw runtime_error("root denominator");stable_sort(roots.begin(),roots.end(),[](auto&a,auto&b){return a.size()>b.size();});uint64_t allnodes=0,closed=0;auto start=chrono::steady_clock::now();for(size_t r=0;r<roots.size();r++){auto t0=chrono::steady_clock::now();fill(begin(member),end(member),false);S.clear();cap=roots[r].size();Dist d;d.fill(14);d[0]=0;HC hc{};for(int u:roots[r]){int v=5*u;d=extend(d,v);S.push_back(v);member[v]=true;for(int k:hs[v])hc[k]++;}d=extend(d,1);S.push_back(1);member[1]=true;for(int k:hs[1])hc[k]++;vector<int>cand;for(int v=1;v<Q;v++)if(v%5&&one_ok(v,d,hc))cand.push_back(v);nodes=prune_size=prune_color=0;maximum=S.size();if(dfs(cand,d,hc))return 2;closed++;if(UINT64_MAX-allnodes<nodes)throw overflow_error("total counter");allnodes+=nodes;double sec=chrono::duration<double>(chrono::steady_clock::now()-t0).count();cout<<"root "<<r<<" h "<<cap<<" pool "<<cand.size()<<" nodes "<<nodes<<" size_prunes "<<prune_size<<" color_prunes "<<prune_color<<" maxdepth "<<maximum<<" seconds "<<sec<<" root_labels";for(int v:roots[r])cout<<' '<<v;cout<<'\n';cout.flush();}cout<<"NORMAL_EXIT denominator "<<roots.size()<<" closed "<<closed<<" total_nodes "<<allnodes<<" seconds "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<'\n';return 0;}catch(exception const&e){cerr<<"ABNORMAL_EXIT "<<e.what()<<'\n';return 3;}}
