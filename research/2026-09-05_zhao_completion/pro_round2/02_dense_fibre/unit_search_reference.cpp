#define main reference_program_entry
#include "search_reference.cpp"
#undef main
static int digit_add(int x,int y){int r=0,s=1;for(int j=0;j<4;j++){r+=((x%5+y%5)%5)*s;x/=5;y/=5;s*=5;}return r;}
int main(){try{
 init();vector<int>sequence={125,125,125,125,25,25,25,25,5,5,5,5,1,1,1,1,6,31,156,37,182};
 vector<uint16_t>sums(1,0);vector<uint8_t>weights(1,0);Dist d;d.fill(14);d[0]=0;uint64_t masks=0,cells=0;
 for(int n=0;n<=21;n++){
  Dist exact;exact.fill(14);for(size_t i=0;i<sums.size();i++){masks++;exact[sums[i]]=min<int>(exact[sums[i]],weights[i]);}
  for(int g=0;g<Q;g++){if(d[g]!=exact[g])throw runtime_error("minimum-length DP mismatch");cells++;}
  if(n==21)break;int v=sequence[n];size_t old=sums.size();sums.resize(2*old);weights.resize(2*old);
  for(size_t i=0;i<old;i++){sums[old+i]=digit_add(sums[i],v);weights[old+i]=weights[i]+1;}d=extend(d,v);
 }
 if(masks!=4194303||cells!=13750)throw runtime_error("test denominator");
 cout<<"NORMAL_EXIT direct_subset_states "<<masks<<" minimum_length_cells "<<cells<<'\n';return 0;
}catch(exception const&e){cerr<<"ABNORMAL_EXIT "<<e.what()<<'\n';return 3;}}
