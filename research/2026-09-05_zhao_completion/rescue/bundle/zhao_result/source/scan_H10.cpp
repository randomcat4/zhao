#include<bits/stdc++.h>
using namespace std;
int ad[125][125],ng[125];
int main(){for(int a=0;a<125;a++)for(int b=0;b<125;b++){int x=a,y=b,p=1,z=0;for(int j=0;j<3;j++){z+=p*((x%5+y%5)%5);x/=5;y/=5;p*=5;}ad[a][b]=z;}
for(int a=0;a<125;a++)for(int b=0;b<125;b++)if(ad[a][b]==0)ng[a]=b;
for(int g=25;g<125;g++)if(g!=25){vector<int>c={1,1,1,5,5,5,25,25,g,g};array<int,125>d;d.fill(99);d[0]=0;bool safe=true;for(int x:c){if(d[ng[x]]<13){safe=false;break;}auto old=d;for(int h=0;h<125;h++)d[ad[h][x]]=min(d[ad[h][x]],old[h]+1);}if(!safe)continue;int n=0;for(int z=0;z<125;z++)if(d[ng[z]]>8)n++;cout<<g<<" "<<n<<endl;}}
