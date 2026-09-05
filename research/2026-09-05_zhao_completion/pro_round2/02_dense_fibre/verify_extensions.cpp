/* Independent exhaustive extension verifier.
   - Reachability: whole-subset bitsets with digit rotations; exact-size fallback.
   - Coloring: degree-ordered first-fit (not the reference color-class routine).
   - Coverage: every raw k-subset is accounted for in an unsigned 128-bit ledger.
   - Every supplied root is processed. There is no time, node, or pool cutoff.
*/
#include <array>
#include <bitset>
#include <vector>
#include <string>
#include <set>
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <numeric>
#include <cstdint>
#include <stdexcept>
#include <chrono>
#include <omp.h>
using namespace std;
using U128=unsigned __int128;
using Bits=bitset<625>;
constexpr int Q=625, NF=156;
static array<int,4> xyz[Q];
static uint16_t plusv[Q][Q], opposite[Q], multiple[5][Q], direction[Q];
static array<uint16_t,6> bad_third[Q][Q];
static vector<int> planes[Q];
static array<uint8_t,6> common_planes[Q][Q];
static Bits prop[Q], nowrap[4][5];
static vector<array<int,4>> forms;
static U128 binomials[500][14];

static string text(U128 n){if(!n)return "0";string s;while(n){s.push_back(char('0'+n%10));n/=10;}reverse(s.begin(),s.end());return s;}
static void add_checked(U128 &a,U128 b){if(~U128(0)-a<b)throw overflow_error("128-bit coverage counter");a+=b;}
static void inc(uint64_t &a){if(a==UINT64_MAX)throw overflow_error("64-bit node counter");++a;}
static int encode(array<int,4>const&a){return 125*a[0]+25*a[1]+5*a[2]+a[3];}
static Bits translated(Bits b,int v){static constexpr int step[4]={125,25,5,1};for(int a=0;a<4;a++){int k=xyz[v][a];if(k)b=((b&nowrap[a][k])<<(k*step[a]))|((b&~nowrap[a][k])>>((5-k)*step[a]));}return b;}
static void initialize(){
 for(int v=0;v<Q;v++){int t=v;for(int a=3;a>=0;a--){xyz[v][a]=t%5;t/=5;}for(int k=0;k<5;k++){auto b=xyz[v];for(int &x:b)x=k*x%5;multiple[k][v]=encode(b);}opposite[v]=multiple[4][v];if(v){int lead=0;while(!xyz[v][lead])lead++;int inv=1;while(inv*xyz[v][lead]%5!=1)inv++;direction[v]=multiple[inv][v];for(int k=1;k<5;k++)prop[v].set(multiple[k][v]);}for(int a=0;a<4;a++)for(int k=1;k<5;k++)if(xyz[v][a]+k<5)nowrap[a][k].set(v);}
 for(int x=0;x<Q;x++)for(int y=0;y<Q;y++){auto a=xyz[x];for(int j=0;j<4;j++)a[j]=(a[j]+xyz[y][j])%5;plusv[x][y]=encode(a);}
 for(int x=1;x<Q;x++)for(int y=1;y<Q;y++){int t=plusv[x][y];bad_third[x][y]={multiple[2][t],multiple[3][t],plusv[multiple[2][x]][opposite[y]],plusv[multiple[3][x]][opposite[y]],plusv[multiple[2][y]][opposite[x]],plusv[multiple[3][y]][opposite[x]]};}
 for(int v=1;v<Q;v++)if(direction[v]==v)forms.push_back(xyz[v]);if(forms.size()!=NF)throw runtime_error("156 functionals");
 for(int v=1;v<Q;v++){for(int f=0;f<NF;f++){int dot=0;for(int a=0;a<4;a++)dot+=xyz[v][a]*forms[f][a];if(dot%5==0)planes[v].push_back(f);}if(planes[v].size()!=31)throw runtime_error("31 planes through each nonzero point");}
 for(int x=1;x<Q;x++)for(int y=1;y<Q;y++)if(direction[x]!=direction[y]){vector<int>a;set_intersection(planes[x].begin(),planes[x].end(),planes[y].begin(),planes[y].end(),back_inserter(a));if(a.size()!=6)throw runtime_error("6 planes through independent pair");copy(a.begin(),a.end(),common_planes[x][y].begin());}
 // Exhaustive translation unit test: all 625*625 point/translation pairs.
 for(int v=0;v<Q;v++)for(int x=0;x<Q;x++){Bits b;b.set(x);Bits r=translated(b,v);if(r.count()!=1||!r[plusv[x][v]])throw runtime_error("digit-rotation unit test");}
 for(int n=0;n<500;n++){binomials[n][0]=1;for(int k=1;k<14;k++){if(k>n)binomials[n][k]=0;else if(k==n)binomials[n][k]=1;else{binomials[n][k]=binomials[n-1][k-1];add_checked(binomials[n][k],binomials[n-1][k]);}}}
}
struct Reach {Bits at_most_11,at_most_12;};
struct Found {vector<int> values;};
struct Outcome {int h=0,pool=0,maximum=0;uint64_t nodes=0,color_prunes=0,size_prunes=0,fallbacks=0;U128 expected=0,closed=0;double seconds=0;string error;vector<int> witness;};
struct Engine {
 int h;vector<int> selected;Bits members;array<uint8_t,NF> counts{};
 uint64_t nodes=0,color_prunes=0,size_prunes=0,fallbacks=0;int maximum=0;
 explicit Engine(int cap):h(cap){}
 Reach reachable(Bits const&whole,int sum){Reach r;int n=selected.size();if(n<=11){r.at_most_11=r.at_most_12=whole;}else if(n==12){r.at_most_12=whole;r.at_most_11=whole;if(!sum)throw runtime_error("a forbidden zero-free prefix sum");r.at_most_11.reset(sum);}else{inc(fallbacks);array<Bits,13>exact;exact[0].set(0);int done=0;for(int v:selected){for(int k=min(12,done+1);k>=1;k--)exact[k]|=translated(exact[k-1],v);done++;}for(int k=0;k<=11;k++)r.at_most_11|=exact[k];r.at_most_12=r.at_most_11|exact[12];}return r;}
 void push(int v){selected.push_back(v);members.set(v);for(int f:planes[v]){if(counts[f]>=h)throw runtime_error("hyperplane capacity exceeded");counts[f]++;}}
 void pop(int v){for(int f:planes[v])counts[f]--;members.reset(v);if(selected.back()!=v)throw runtime_error("stack mismatch");selected.pop_back();}
 bool capacity(int v)const{for(int f:planes[v])if(counts[f]>=h)return false;return true;}
 bool compatible(int x,int y,Reach const&r)const{if(direction[x]==direction[y]||r.at_most_11[opposite[plusv[x][y]]])return false;for(int v:bad_third[x][y])if(members[v])return false;for(int f:common_planes[x][y])if(counts[f]>=h-1)return false;return true;}
 U128 visit(vector<int>const&candidates,Bits const&whole,int sum,Bits const&forbidden){
  inc(nodes);maximum=max(maximum,(int)selected.size());int need=21-selected.size(),n=candidates.size();
  if(!need)throw Found{selected};if(need<0||need>13||n>499)throw runtime_error("state outside proved bounds");
  U128 expected=binomials[n][need],closed=0;if(n<need){inc(size_prunes);return 0;}
  Reach r=reachable(whole,sum);vector<bitset<512>>edges(n);vector<int>degree(n,0);
  for(int i=0;i<n;i++)for(int j=0;j<i;j++)if(compatible(candidates[i],candidates[j],r)){edges[i].set(j);edges[j].set(i);degree[i]++;degree[j]++;}
  // First-fit proper vertex coloring in decreasing degree order.
  vector<int>priority(n);iota(priority.begin(),priority.end(),0);sort(priority.begin(),priority.end(),[&](int x,int y){return degree[x]!=degree[y]?degree[x]>degree[y]:candidates[x]<candidates[y];});
  vector<int>color(n,-1);for(int pos=0;pos<n;pos++){int v=priority[pos];bitset<512>used;for(int j=0;j<pos;j++){int u=priority[j];if(edges[v][u])used.set(color[u]);}int c=0;while(used[c])c++;color[v]=c;}
  // Independently validate every color class before using it as an upper bound.
  vector<bitset<512>> classes(n);for(int v=0;v<n;v++){if(color[v]<0||color[v]>=n||(edges[v]&classes[color[v]]).any())throw runtime_error("invalid coloring certificate");classes[color[v]].set(v);}
  vector<int>order(n);iota(order.begin(),order.end(),0);sort(order.begin(),order.end(),[&](int x,int y){return color[x]!=color[y]?color[x]<color[y]:candidates[x]<candidates[y];});
  for(int i=n-1;i>=0;i--){int ix=order[i];if(color[ix]+1<need){inc(color_prunes);add_checked(closed,binomials[i+1][need]);break;}
   int v=candidates[ix];Bits next_bad=forbidden|prop[v];for(int x:selected)for(int z:bad_third[x][v])next_bad.set(z);
   Bits next_whole=whole|translated(whole,v);int next_sum=plusv[sum][v];push(v);Reach nr=reachable(next_whole,next_sum);
   vector<int>next;for(int j=0;j<i;j++){int u=candidates[order[j]];if(edges[ix][order[j]]&&!next_bad[u]&&!nr.at_most_12[opposite[u]]&&capacity(u))next.push_back(u);}
   U128 raw=binomials[i][need-1],surviving=binomials[next.size()][need-1];if(surviving>raw)throw runtime_error("coverage partition underflow");add_checked(closed,raw-surviving);
   if(surviving)add_checked(closed,visit(next,next_whole,next_sum,next_bad));else inc(size_prunes);
   pop(v);
  }
  if(closed!=expected)throw runtime_error("node coverage mismatch");return closed;
 }
 Outcome run(vector<int>const&root){Outcome o;o.h=h;auto t0=chrono::steady_clock::now();try{Bits whole;whole.set(0);Bits bad;int sum=0;for(int x:root){int v=5*x;if(whole[opposite[v]]||bad[v])throw runtime_error("invalid root");Bits newbad=bad|prop[v];for(int y:selected)for(int z:bad_third[y][v])newbad.set(z);bad=newbad;whole|=translated(whole,v);sum=plusv[sum][v];push(v);}int v=1;Bits newbad=bad|prop[v];for(int y:selected)for(int z:bad_third[y][v])newbad.set(z);bad=newbad;whole|=translated(whole,v);sum=plusv[sum][v];push(v);Reach r=reachable(whole,sum);vector<int>cand;for(int x=1;x<Q;x++)if(x%5&&!bad[x]&&!r.at_most_12[opposite[x]]&&capacity(x))cand.push_back(x);o.pool=cand.size();int need=20-h;o.expected=binomials[499][need];o.closed=o.expected-binomials[cand.size()][need];add_checked(o.closed,visit(cand,whole,sum,bad));if(o.closed!=o.expected)throw runtime_error("root denominator mismatch");}catch(Found const&f){o.witness=f.values;}catch(exception const&e){o.error=e.what();}o.nodes=nodes;o.color_prunes=color_prunes;o.size_prunes=size_prunes;o.fallbacks=fallbacks;o.maximum=maximum;o.seconds=chrono::duration<double>(chrono::steady_clock::now()-t0).count();return o;}
};
int main(int argc,char**argv){try{if(argc<2||argc>3)throw runtime_error("usage verify_extensions ROOTS [THREADS]");int threads=argc==3?stoi(argv[2]):1;if(threads<1)throw runtime_error("threads must be positive");initialize();ifstream f(argv[1]);if(!f)throw runtime_error("missing root file");vector<vector<int>>roots;set<vector<int>>distinct;array<int,10>hc{};string line;while(getline(f,line)){istringstream in(line);int n,x;in>>n;vector<int>a;while(in>>x)a.push_back(x);if(n<7||n>9||(int)a.size()!=n||!is_sorted(a.begin(),a.end())||adjacent_find(a.begin(),a.end())!=a.end()||a.front()<1||a.back()>124)throw runtime_error("malformed root");if(!distinct.insert(a).second)throw runtime_error("duplicate root");roots.push_back(a);hc[n]++;}if(roots.size()!=1786||hc[7]!=1084||hc[8]!=659||hc[9]!=43)throw runtime_error("root census mismatch");vector<Outcome>result(roots.size());auto start=chrono::steady_clock::now();
 #pragma omp parallel for schedule(dynamic,1) num_threads(threads)
 for(int i=0;i<(int)roots.size();i++){Engine e(roots[i].size());result[i]=e.run(roots[i]);
  #pragma omp critical
  {auto const&o=result[i];cout<<"root "<<i<<" h "<<o.h<<" pool "<<o.pool<<" nodes "<<o.nodes<<" color_prunes "<<o.color_prunes<<" size_prunes "<<o.size_prunes<<" maxdepth "<<o.maximum<<" fallbacks "<<o.fallbacks<<" expected "<<text(o.expected)<<" closed "<<text(o.closed)<<" seconds "<<o.seconds<<" labels";for(int x:roots[i])cout<<' '<<x;if(!o.error.empty())cout<<" ERROR "<<o.error;if(!o.witness.empty()){cout<<" FOUND";for(int x:o.witness)cout<<' '<<x;}cout<<'\n';cout.flush();}
 }
 U128 expected=0,closed=0;uint64_t total_nodes=0,fb=0;int complete=0,depth=0;bool found=false;for(auto const&o:result){if(!o.error.empty())throw runtime_error(o.error);if(!o.witness.empty()){found=true;continue;}if(o.expected!=o.closed)throw runtime_error("final coverage mismatch");add_checked(expected,o.expected);add_checked(closed,o.closed);if(UINT64_MAX-total_nodes<o.nodes||UINT64_MAX-fb<o.fallbacks)throw overflow_error("summary counter");total_nodes+=o.nodes;fb+=o.fallbacks;depth=max(depth,o.maximum);complete++;}if(found)return 2;if(complete!=1786)throw runtime_error("incomplete root loop");cout<<"NORMAL_EXIT roots "<<complete<<"/1786 expected "<<text(expected)<<" closed "<<text(closed)<<" total_nodes "<<total_nodes<<" maximum_depth "<<depth<<" exact_size_fallbacks "<<fb<<" translation_tests 390625 seconds "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<'\n';return 0;}catch(exception const&e){cerr<<"ABNORMAL_EXIT "<<e.what()<<'\n';return 3;}}
