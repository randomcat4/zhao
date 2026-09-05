/* Exhaustive basis-normalized rank-three enumeration and GL(3,5) orbits.
   No pool, time, or node cutoff. The assertion at size 13 is I^13=0, not a prune.
   The independent Python verifier uses different subset-sum and inverse routines. */
#include <array>
#include <bitset>
#include <vector>
#include <set>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <cstdint>
#include <stdexcept>
using namespace std;
static int addition[125][125],negative[125],timesv[5][125],directionv[125];
static vector<int> selected={25,5,1};
static array<uint64_t,14> counts{};static uint64_t nodes=0;static int maximum=3;
static array<set<vector<int>>,13> pool;
static array<int,3> digits(int x){return {x/25,x/5%5,x%5};}
static int encode(array<int,3>a){return 25*a[0]+5*a[1]+a[2];}
static void bump(uint64_t&x){if(x==UINT64_MAX)throw overflow_error("counter");x++;}
static void setup(){for(int x=0;x<125;x++){auto a=digits(x);for(int c=0;c<5;c++){auto b=a;for(int&v:b)v=c*v%5;timesv[c][x]=encode(b);}negative[x]=timesv[4][x];if(x){int lead=0;while(!a[lead])lead++;int k=1;while(k*a[lead]%5!=1)k++;directionv[x]=timesv[k][x];}for(int y=0;y<125;y++){auto b=digits(y);for(int j=0;j<3;j++)b[j]=(a[j]+b[j])%5;addition[x][y]=encode(b);}}}
static bool admissible(int v){for(int x:selected)if(directionv[x]==directionv[v])return false;for(size_t i=0;i<selected.size();i++)for(size_t j=0;j<i;j++){int x=selected[i],y=selected[j];for(int c:{2,3})if(addition[x][y]==timesv[c][v]||addition[v][x]==timesv[c][y]||addition[v][y]==timesv[c][x])return false;}return true;}
static void enumerate(int lower,bitset<125>const&sums){int n=selected.size();if(n>=13)throw runtime_error("zero-free set contradicts I^13=0");bump(nodes);bump(counts[n]);maximum=max(maximum,n);if(n>=7){auto a=selected;sort(a.begin(),a.end());if(!pool[n].insert(a).second)throw runtime_error("duplicate enumeration");}for(int v=lower;v<125;v++){if(v==1||v==5||v==25||sums[negative[v]]||!admissible(v))continue;auto next=sums;for(int x=0;x<125;x++)if(sums[x])next.set(addition[x][v]);selected.push_back(v);enumerate(v+1,next);selected.pop_back();}}
static bool inverse(vector<int>const&basis,int out[3][3]){int a[3][6]{};for(int c=0;c<3;c++){auto v=digits(basis[c]);for(int r=0;r<3;r++)a[r][c]=v[r];}for(int r=0;r<3;r++)a[r][r+3]=1;for(int c=0;c<3;c++){int r=c;while(r<3&&!a[r][c])r++;if(r==3)return false;for(int j=0;j<6;j++)swap(a[c][j],a[r][j]);int u=1;while(u*a[c][c]%5!=1)u++;for(int j=0;j<6;j++)a[c][j]=u*a[c][j]%5;for(int k=0;k<3;k++)if(k!=c){int t=a[k][c];for(int j=0;j<6;j++)a[k][j]=(a[k][j]-t*a[c][j]+25)%5;}}for(int r=0;r<3;r++)for(int c=0;c<3;c++)out[r][c]=a[r][c+3];return true;}
static vector<int> transform(vector<int>const&s,int a[3][3]){vector<int>result;for(int v:s){auto x=digits(v);array<int,3>y{};for(int r=0;r<3;r++)for(int c=0;c<3;c++)y[r]=(y[r]+a[r][c]*x[c])%5;result.push_back(encode(y));}sort(result.begin(),result.end());return result;}
int main(int argc,char**argv){try{if(argc!=2)throw runtime_error("usage generate_roots OUTPUT");setup();bitset<125>sums;sums.set(0);for(int v:selected){auto next=sums;for(int x=0;x<125;x++)if(sums[x])next.set(addition[x][v]);sums=next;}enumerate(1,sums);if(maximum!=9)throw runtime_error("unexpected maximum; no bound certified");ofstream out(argv[1]);if(!out)throw runtime_error("cannot open output");uint64_t all=0,removed_total=0;for(int h=7;h<=9;h++){auto denominator=pool[h].size();set<vector<int>>roots;uint64_t removed=0;while(!pool[h].empty()){auto root=*pool[h].begin();set<vector<int>>orbit;int a[3][3];for(int x:root)for(int y:root)if(y!=x)for(int z:root)if(z!=x&&z!=y&&inverse({x,y,z},a))orbit.insert(transform(root,a));if(orbit.empty())throw runtime_error("rank deficient root");roots.insert(*orbit.begin());for(auto const&im:orbit){if(pool[h].erase(im)!=1)throw runtime_error("missing or repeated orbit image");bump(removed);}}if(removed!=denominator)throw runtime_error("orbit denominator mismatch");for(auto const&r:roots){out<<h;for(int v:r)out<<' '<<v;out<<'\n';}cout<<"size "<<h<<" normalized "<<denominator<<" removed "<<removed<<" orbits "<<roots.size()<<'\n';all+=roots.size();removed_total+=removed;}out.close();if(!out)throw runtime_error("output write failed");if(all!=1786||removed_total!=406416||nodes!=450754)throw runtime_error("unexpected census");cout<<"NORMAL_EXIT roots "<<all<<" normalized "<<removed_total<<" nodes "<<nodes<<" maximum "<<maximum<<'\n';for(int n=3;n<=12;n++)cout<<"size_count "<<n<<' '<<counts[n]<<'\n';return 0;}catch(exception const&e){cerr<<"ABNORMAL_EXIT "<<e.what()<<'\n';return 3;}}
