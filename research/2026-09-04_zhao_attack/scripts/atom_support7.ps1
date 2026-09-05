$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

# Exact check for seven support elements with all multiplicities at most 3.
# No packages, network access, randomness, or floating-point arithmetic.
$atomCode = @'
using System;
using System.Diagnostics;

public static class AtomSupportSeven {
    static int[,] digit = new int[625,4];
    static int[] support = new int[620];
    static int neg5(int x) { int r=x%5; return r==0 ? 0 : 5-r; }

    // Return the coordinates that may be reduced from multiplicity 3 to 2.
    // A bit can be used in case B only for a nonempty zero sum of length <=14.
    // The separate bit 7 records the existence of a length <=13 zero sum.
    static int witness(int a,int b,int c,int t,int u,int v) {
        int length=t+u+v;
        int mask=(t<=2?16:0)|(u<=2?32:0)|(v<=2?64:0);
        for(int j=0;j<4;j++) {
            int x=neg5(t*digit[a,j]+u*digit[b,j]+v*digit[c,j]);
            if(x==4) return 0;
            length+=x;
            if(x<=2) mask|=1<<j;
        }
        if(length==0 || length>14) return 0;
        if(length<=13) mask|=128;
        return mask;
    }

    static void ReportBad(int a,int b,int c,int flags) {
        Console.WriteLine("BAD a="+a+" b="+b+" c="+c+" flags="+flags);
    }

    public static void Run() {
        var watch=Stopwatch.StartNew();
        int q=0;
        for(int x=0;x<625;x++) {
            int z=x;
            for(int j=0;j<4;j++) { digit[x,j]=z%5; z/=5; }
            if(x!=0 && x!=1 && x!=5 && x!=25 && x!=125) support[q++]=x;
        }
        if(q!=620) throw new Exception("Support construction failed");
        long matrices=0, pairPruned=0, cScanned=0, badA=0, badB=0;
        long badMatrices=0, vectorChecks=0;
        for(int ia=0;ia<618;ia++) {
            int a=support[ia];
            for(int ib=ia+1;ib<619;ib++) {
                int b=support[ib], flags=0;
                // All relations that omit c are reusable for every c>b.
                for(int t=0;t<=3 && flags!=255;t++) {
                    for(int u=0;u<=3 && flags!=255;u++) {
                        if(t==0 && u==0) continue;
                        flags|=witness(a,b,0,t,u,0); vectorChecks++;
                    }
                }
                if(flags==255) {
                    long count=619-ib;
                    matrices+=count; pairPruned+=count;
                    continue;
                }
                for(int ic=ib+1;ic<620;ic++) {
                    int c=support[ic], f=flags;
                    matrices++; cScanned++;
                    for(int v=1;v<=3 && f!=255;v++)
                        for(int t=0;t<=3 && f!=255;t++)
                            for(int u=0;u<=3 && f!=255;u++) {
                                f|=witness(a,b,c,t,u,v); vectorChecks++;
                            }
                    if(f!=255) {
                        if((f&128)==0) badA++;
                        for(int j=0;j<7;j++) if((f&(1<<j))==0) badB++;
                        badMatrices++;
                        if(badMatrices<=20) ReportBad(a,b,c,f);
                    }
                }
            }
            if(ia%100==0) Console.WriteLine("PROGRESS ia="+ia+" matrices="+matrices+" seconds="+watch.Elapsed.TotalSeconds.ToString("F2"));
        }
        const long expected=39529340;
        if(matrices!=expected) throw new Exception("Matrix total differs from binomial(620,3)");
        Console.WriteLine("RESULT matrices="+matrices+" pair_pruned="+pairPruned+" c_scanned="+cScanned+" vector_checks="+vectorChecks+" bad_A="+badA+" bad_B_patterns="+badB+" bad_matrices="+badMatrices+" seconds="+watch.Elapsed.TotalSeconds.ToString("F2"));
    }
}
'@
Add-Type -TypeDefinition $atomCode -Language CSharp
[AtomSupportSeven]::Run()
