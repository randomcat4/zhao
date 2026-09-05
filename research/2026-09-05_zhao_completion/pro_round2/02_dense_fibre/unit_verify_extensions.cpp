// Finite boundary tests for the implementation, not a global theorem by itself.
#define main full_verifier_entry
#include "verify_extensions.cpp"
#undef main
static int direct_add(int x,int y){int r=0,s=1;for(int j=0;j<4;j++){r+=((x%5+y%5)%5)*s;x/=5;y/=5;s*=5;}return r;}
int main(){try{
 initialize();uint64_t third_tests=0,pair_tests=0;
 for(int x=1;x<Q;x++)for(int y=x+1;y<Q;y++)if(direction[x]!=direction[y]){
  Bits listed;for(int z:bad_third[x][y])listed.set(z);pair_tests++;
  for(int z=0;z<Q;z++){
   bool direct=false;
   if(z&&z!=x&&z!=y)for(int c:{2,3})direct=direct||plusv[x][y]==multiple[c][z]||plusv[x][z]==multiple[c][y]||plusv[y][z]==multiple[c][x];
   if(listed[z]!=direct)throw runtime_error("third-point interface mismatch");third_tests++;
  }
 }
 if(pair_tests!=193440||third_tests!=120900000)throw runtime_error("geometry denominator");
 vector<int>sequence={125,125,125,125,25,25,25,25,5,5,5,5,1,1,1,1,6,31,156,37,182};
 vector<uint16_t>sums(1,0);vector<uint8_t>weights(1,0);Bits whole;whole.set(0);int sum=0;Engine e(30);uint64_t masks=0,comparisons=0;
 for(int n=0;n<=21;n++){
  Reach r=e.reachable(whole,sum);Bits expected11,expected12;
  for(size_t i=0;i<sums.size();i++){masks++;if(weights[i]<=11)expected11.set(sums[i]);if(weights[i]<=12)expected12.set(sums[i]);}
  if(r.at_most_11!=expected11||r.at_most_12!=expected12)throw runtime_error("cardinality boundary mismatch");comparisons+=1250;
  if(n==21)break;int v=sequence[n];size_t old=sums.size();sums.resize(2*old);weights.resize(2*old);
  for(size_t i=0;i<old;i++){sums[old+i]=direct_add(sums[i],v);weights[old+i]=weights[i]+1;}
  whole|=translated(whole,v);sum=direct_add(sum,v);e.selected.push_back(v);
 }
 if(masks!=4194303||comparisons!=27500||e.fallbacks!=9)throw runtime_error("reachability test denominator");
 uint64_t binomial_tests=0;
 for(int n=0;n<500;n++)for(int k=0;k<14;k++){
  U128 value=0;if(k<=n){value=1;for(int j=1;j<=k;j++){U128 product=value*(n-j+1);if(product%j)throw runtime_error("nonintegral binomial recurrence");value=product/j;}}
  if(value!=binomials[n][k])throw runtime_error("binomial mismatch");binomial_tests++;
 }
 cout<<"NORMAL_EXIT independent_pairs "<<pair_tests<<" third_point_tests "<<third_tests<<" direct_subset_states "<<masks<<" reachability_cells "<<comparisons<<" exact_size_boundaries "<<e.fallbacks<<" binomial_cells "<<binomial_tests<<" translation_tests 390625\n";return 0;
}catch(exception const&e){cerr<<"ABNORMAL_EXIT "<<e.what()<<'\n';return 3;}}
