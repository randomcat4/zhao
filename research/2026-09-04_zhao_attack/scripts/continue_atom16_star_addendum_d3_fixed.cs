// Targeted exhaustive test of the two normalized d=3, M=1 star cores.
// No SAT/random search and no imports from project search implementations.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

public static class ContinueAtom16StarAddendumD3Fixed {
    const int Q=625, Cutoff=14;
    static readonly int[] plus=new int[Q*Q], neg=new int[Q];
    static readonly Stopwatch timer=new Stopwatch();
    static double secondsLimit;
    static bool timedOut, found;
    static long[] nodes=new long[8];
    static long leafSumTests;
    static int[] witness;
    static int targetSum;
    static bool[] forbidden=new bool[Q];
    static int Add(int x,int y){int z=0,p=1;for(int k=0;k<4;k++,p*=5){z+=((x%5+y%5)%5)*p;x/=5;y/=5;}return z;}
    static byte[] AddPosition(byte[] old,int g){var next=(byte[])old.Clone();for(int h=0;h<Q;h++){int d=old[h]+1;if(d<99){int t=plus[h*Q+g];if(d<next[t])next[t]=(byte)d;}}return next;}
    static bool Safe(byte[] d,int g){return d[neg[g]]>=Cutoff;}
    static void Search(byte[] state,List<int> extras,int sum,bool duplicateUsed){
        if(timedOut||found)return;
        int depth=extras.Count;nodes[depth]++;
        if((nodes.Sum()&16383)==0&&timer.Elapsed.TotalSeconds>secondsLimit){timedOut=true;return;}
        if(depth==7){leafSumTests++;if(sum==targetSum){found=true;witness=extras.ToArray();}return;}
        int last=depth==0?0:extras[depth-1];
        if(depth==6){
            int needed=plus[targetSum*Q+neg[sum]];
            bool repeat=depth>0&&needed==last;
            if(needed<last||forbidden[needed]||(!repeat&&extras.Contains(needed))||(repeat&&(duplicateUsed||depth>1&&extras[depth-2]==last))||!Safe(state,needed))return;
            var next=AddPosition(state,needed);extras.Add(needed);Search(next,extras,targetSum,duplicateUsed||repeat);extras.RemoveAt(depth);return;
        }
        for(int g=last;g<Q;g++){
            if(forbidden[g])continue;
            bool repeat=depth>0&&g==last;
            if(repeat&&(duplicateUsed||depth>1&&extras[depth-2]==last))continue;
            if(!repeat&&extras.Contains(g))continue;
            if(!Safe(state,g))continue;
            var next=AddPosition(state,g);extras.Add(g);
            Search(next,extras,plus[sum*Q+g],duplicateUsed||repeat);
            extras.RemoveAt(depth);if(timedOut||found)return;
        }
    }
    static object RunCore(string name,int[] values,int[] caps,bool excludeForcedSupport){
        Array.Clear(nodes,0,nodes.Length);leafSumTests=0;timedOut=false;found=false;witness=null;
        Array.Clear(forbidden,0,forbidden.Length);if(excludeForcedSupport)foreach(int g in values)forbidden[g]=true;
        var state=new byte[Q];for(int g=1;g<Q;g++)state[g]=99;
        for(int i=0;i<values.Length;i++)for(int k=0;k<caps[i];k++){
            if(!Safe(state,values[i]))throw new Exception("forced core already has short zero");
            state=AddPosition(state,values[i]);
        }
        // The 16-atom T has x,g1,y1^3,y2^2,y3^2 plus seven W positions.
        int[] forcedT={1,6,5,5,5,25,25,125,125};int s=0;foreach(int g in forcedT)s=plus[s*Q+g];targetSum=neg[s];
        timer.Restart();Search(state,new List<int>(),0,false);timer.Stop();
        return new {name,exclude_forced_support=excludeForcedSupport,complete=!timedOut,timed_out=timedOut,found_safe_B20_witness=found,
            target_W_sum=targetSum,nodes_by_W_length=(long[])nodes.Clone(),leaf_sum_tests=leafSumTests,witness_W=witness};
    }
    static string Hash(string p)=>Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(p))).ToLowerInvariant();
    public static void Run(string root,double limit){
        secondsLimit=limit;
        for(int g=0;g<Q;g++){for(int h=0;h<Q;h++)plus[g*Q+h]=Add(g,h);int z=0,p=1,x=g;for(int k=0;k<4;k++,p*=5){z+=((5-x%5)%5)*p;x/=5;}neg[g]=z;}
        int[] values={1,6,5,26,25,126,125};
        var first=RunCore("k=(2,1,1), m on the k=2 value",values,new[]{1,3,3,1,2,1,2},true);
        var second=RunCore("k=(2,1,1), m on a k=1 value",values,new[]{1,2,3,2,2,1,2},true);
        var firstRelaxed=RunCore("k=(2,1,1), m on the k=2 value",values,new[]{1,3,3,1,2,1,2},false);
        var secondRelaxed=RunCore("k=(2,1,1), m on a k=1 value",values,new[]{1,2,3,2,2,1,2},false);
        string[] inputs={"proofs/continue_atom16_star.md","proofs/continue_atom16_star_addendum.md","scripts/continue_atom16_star_addendum_d3_fixed.cs","scripts/continue_atom16_star_addendum_d3_fixed.ps1"};
        var hashes=inputs.ToDictionary(x=>x,x=>Hash(Path.Combine(root,x)));
        var output=new {status="TARGETED_D3_M1_EXHAUSTIVE_EXTENSION_TEST_FIXED",scope="Two forced normalized 13-position cores; W has seven positions and at most one doubled value",corrected_defect="Each RunCore result now owns a cloned nodes_by_W_length snapshot; the frozen original evidence aliased the static nodes array",cores_with_true_support_filter=new[]{first,second},support_relaxed_all_625_values_crosscheck=new[]{firstRelaxed,secondRelaxed},input_sha256=hashes};
        File.WriteAllText(Path.Combine(root,"evidence/continue_atom16_star_addendum_d3_fixed.json"),JsonSerializer.Serialize(output,new JsonSerializerOptions{WriteIndented=true})+"\n",new UTF8Encoding(false));
        Console.WriteLine(JsonSerializer.Serialize(new{output.status,output.cores_with_true_support_filter,output.support_relaxed_all_625_values_crosscheck}));
    }
}
