"""All-prime necessary completion test for the surviving M1 x components.

Other components are independent relaxations; finding a completion is not a
construction. A missing completion excludes the entire input scalar case.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import json
from verify_double_star_survivors import residue_affine, add, neg, interval


def catalogue(V, mod, allowed, maxn):
    twiceV = int(2*V)
    assert F(twiceV) == 2*V
    mass = {"x":4,"u":4,"t":4,"v":-6,"z":twiceV,"h":-6-twiceV}
    degree = {"x":14,"u":-2-twiceV,"t":4+twiceV,"v":-2,"z":-2,"h":-2}
    out = []
    tested = 0
    free = 0
    maxres = 0
    for size in range(1,len(allowed)+1):
        for names in combinations(allowed,size):
            for n in range(size,maxn+1):
                for locations in permutations(range(n),size):
                    pos=dict(zip(names,locations))
                    rhs=[2]*n
                    for name,i in pos.items():rhs[i]=degree[name]
                    for loop in [False,True]:
                        forms=[(1,0),(-int(loop),rhs[0]+4*loop)]
                        for i in range(1,n):
                            a,c=forms[i-1];forms.append((-a,rhs[i]-c))
                        eq=[forms[-1]]+[(forms[i][0],forms[i][1]-mass[name]) for name,i in pos.items()]
                        bad=[abs(c) for a,c in eq if a==0 and c]
                        pivot=next((r for r in eq if r[0]),None)
                        if pivot:
                            a,c=pivot
                            assert abs(a)==1
                            bad += [abs(a*cc-aa*c) for aa,cc in eq if a*cc-aa*c]
                        tested+=1
                        if bad:
                            assert min(bad)<149
                            maxres=max(maxres,min(bad))
                            continue
                        conditions=[]
                        if pivot:
                            T=-c//a
                            masses=[residue_affine(F(aa*T+cc,4),mod) for aa,cc in forms[:-1]]
                            for m in masses:conditions += [add(m,(0,-1)),add((1,-4),neg(m))]
                            total=add(*masses)
                        else:
                            T="free"
                            free+=1
                            total=add((0,n-len(names)),*(residue_affine(F(mass[name],4),mod) for name in names))
                        if loop:conditions.append(add((2,-2),neg(total)))
                        possible=interval(conditions)
                        if possible is not None:
                            out.append({"n":n,"labels":frozenset(names),"positions":pos,"loop":loop,
                                        "T":T,"mass":total,"conditions":conditions})
    return out,{"arrangements":tested,"raw_free_cases":free,"max_residual":maxres,"necessary_candidates":len(out)}


def search(left,vertices,mass,conditions,candidates,chosen):
    if not left:
        feasible=interval(conditions+[add((3,-3),neg(mass))])
        if feasible is not None:
            return chosen,feasible,mass
        return None
    anchor=sorted(left)[0]
    for c in candidates:
        if anchor not in c["labels"] or not c["labels"]<=left or c["n"]>vertices:continue
        total=add(mass,c["mass"])
        cond=conditions+c["conditions"]
        if interval(cond+[add((3,-3),neg(total))]) is None:continue
        result=search(left-c["labels"],vertices-c["n"],total,cond,candidates,chosen+[c])
        if result is not None:return result
    return None


def completion_certificates(left,vertices,mass,conditions,candidates,chosen):
    """Enumerate all structurally possible completions before global capacity."""
    if not left:
        domain=interval(conditions)
        if domain is None:return []
        a,b=mass[0]-3,mass[1]+3
        lo,hi=domain
        if a>=0:gap=a*lo+b
        else:
            assert hi is not None
            gap=a*hi+b
        assert gap>0,(chosen,domain,mass)
        return [{"components":[{"labels":sorted(q["labels"]),"n":q["n"],"positions":q["positions"],"loop":q["loop"]} for q in chosen],
                 "total_mass":[str(q) for q in mass],"p_domain":[str(q) for q in domain],
                 "minimum_excess_over_3p_minus3":str(gap)}]
    anchor=sorted(left)[0]
    out=[]
    for c in candidates:
        if anchor not in c["labels"] or not c["labels"]<=left or c["n"]>vertices:continue
        cond=conditions+c["conditions"]
        if interval(cond) is None:continue
        out+=completion_certificates(left-c["labels"],vertices-c["n"],add(mass,c["mass"]),cond,candidates,chosen+[c])
    return out


def main():
    root=Path(__file__).parent
    inp=json.loads((root/"M1_generic_survivor_audit.json").read_text())["remaining"]
    reports=[]
    cache={}
    for q in inp:
        assert "unclosed_free" not in q
        V,T,mod=F(q["V"]),F(q["T"]),q["mod4"]
        xmass=add(*(residue_affine((a*T+b*V+c)/2,mod) for a,b,c in q["forms"]))
        cond=[add((2,-2),neg(xmass))] if q["loop"] else []
        if interval(cond) is None:
            reports.append({"input":q,"status":"EXCLUDED_LOOP_RANK_TWO"})
            continue
        missing=frozenset({"x","u","t","v","z","h"}-set(q["positions"]))
        key=(V,mod,tuple(sorted(missing)),17-q["n"])
        if key not in cache:
            cache[key]=catalogue(V,mod,tuple(sorted(missing)),17-q["n"])
        candidates,stats=cache[key]
        represented=frozenset().union(*(c["labels"] for c in candidates))
        absent=sorted(missing-represented)
        result=search(missing,17-q["n"],xmass,cond,candidates,[])
        report={"input":q,"catalogue_stats":stats,"unrepresented_special_values":absent,
                "status":"POTENTIAL_COMPLETION" if result else "EXCLUDED_NO_COMPLETION"}
        if result:
            chosen,bounds,total=result
            report["completion"]=[{k:sorted(v) if isinstance(v,frozenset) else v for k,v in c.items() if k!="conditions"} for c in chosen]
            report["p_interval"]=[str(v) for v in bounds]
            report["total_mass_lower_bound"]=[str(v) for v in total]
        else:
            report["complete_partition_certificates"]=completion_certificates(missing,17-q["n"],xmass,cond,candidates,[])
        reports.append(report)
        print(V,mod,q["positions"],report["status"],stats,flush=True)
        (root/"M1_component_completion.json").write_text(json.dumps(reports,indent=2,default=str)+"\n")
    (root/"M1_component_completion.json").write_text(json.dumps(reports,indent=2,default=str)+"\n")
    print("done",len(reports),"potential",sum(q["status"]=="POTENTIAL_COMPLETION" for q in reports))


if __name__=="__main__":main()
