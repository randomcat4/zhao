"""Generate exact rational Farkas certificates for all critical collision LPs.

HiGHS only proposes certificate supports. Every certificate is solved and
checked over Fraction before it is written. Remaining patterns need hand proofs.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import gzip
import json
import time
from scipy.optimize import linprog
from classify_two_active import collision_cases, make_values


def exact_system(pattern, threshold, lift, ks):
    """Return affine rows <=0; final entry of each row is its constant."""
    r = pattern["residue"]
    groups = pattern["classes"]
    fixed = {
        "t": (F(1,2),F(-1,2)), "v1": (F(1,2),F(-1,2)),
        "v2": (F(1,2),F(-1,2)),
        "u1": (F(lift,r.denominator),F(r.numerator,r.denominator)),
        "u2": (F(1,2)-F(lift,r.denominator),F(5,2)-F(r.numerator,r.denominator)),
    }
    zeros = {"y","b1","b2","b3","u3","v3"}
    unknown = [g for g in groups if not set(g)&(zeros|set(fixed))]
    dim = len(unknown)+1
    def blank(): return [F(0)]*(dim+1)
    expressions = {}
    for g in groups:
        v = blank()
        if set(g)&zeros:
            pass
        elif set(g)&set(fixed):
            name = next(n for n in g if n in fixed)
            v[0],v[-1] = fixed[name]
        else:
            v[unknown.index(g)+1] = 1
        for name in g:
            expressions[name] = tuple(v)
    rows,labels = [],[]
    def put(v,label): rows.append(tuple(v)); labels.append(label)
    v=blank();v[0]=-1;v[-1]=threshold;put(v,"p>=threshold")
    for i,g in enumerate(unknown):
        v=blank();v[i+1]=-1;put(v,"nonnegative:"+','.join(g))
    for g in groups:
        v=list(expressions[g[0]]);v[0]-=1;v[-1]+=4;put(v,"height:"+','.join(g))
    for name in ["u1","u2"]:
        v=[-x for x in expressions[name]];v[-1]+=1;put(v,"positive:"+name)
    v=[a-b for a,b in zip(expressions["u1"],expressions["u2"])];put(v,"m<=n")
    v=[sum(expressions[g[0]][i] for g in groups) for i in range(dim+1)]
    v[0]-=3;v[-1]+=4;put(v,"position_capacity")
    ids={name:i for i,g in enumerate(groups) for name in g}
    for pos,partners,extra,k in [
        ("t",["r1","r2","r3"],1,ks[0]),
        ("v1",["u1","n12","n13"],0,ks[1]),
        ("v2",["u2","n21","n23"],0,ks[2])]:
        v=[sum(expressions[x][i] for x in partners) for i in range(dim+1)]
        v[-1]+=extra-sum(ids[x]==ids[pos] for x in partners)
        v[0]-=F(1,2)+k;v[-1]-=F(1,2)
        put(v,"degree:"+pos+":positive")
        put([-x for x in v],"degree:"+pos+":negative")
    return rows, labels, unknown


def solve_exact(a,b):
    a=[list(map(F,row))+[F(rhs)] for row,rhs in zip(a,b)]
    n=len(a[0])-1
    pivots=[];i=0
    for j in range(n):
        k=next((k for k in range(i,len(a)) if a[k][j]),None)
        if k is None: continue
        a[i],a[k]=a[k],a[i]
        pivot=a[i][j];a[i]=[x/pivot for x in a[i]]
        for k in range(len(a)):
            if k!=i and a[k][j]:
                q=a[k][j];a[k]=[x-q*y for x,y in zip(a[k],a[i])]
        pivots.append(j);i+=1
        if i==len(a): break
    for row in a:
        if not any(row[:n]) and row[-1]:
            raise ValueError("inconsistent certificate support")
    x=[F(0)]*n
    for row,j in zip(a,pivots): x[j]=row[-1]
    return x


def certificate(rows):
    dim=len(rows[0])-1
    a=[[float(row[j]) for row in rows] for j in range(dim)]
    a.append([1.0]*len(rows))
    result=linprog([-float(row[-1]) for row in rows],A_eq=a,b_eq=[0.0]*dim+[1.0],
                   bounds=(0,None),method="highs")
    if not result.success:
        raise RuntimeError("dual search failed: "+result.message)
    if result.fun >= -1e-9:
        primal=linprog([0.0]*dim,A_ub=[[float(x) for x in row[:-1]] for row in rows],
                       b_ub=[-float(row[-1]) for row in rows],bounds=[(None,None)]*dim,method="highs")
        if not primal.success:
            raise RuntimeError("no verified dual and no feasible primal: "+primal.message)
        return None
    support=[i for i,x in enumerate(result.x) if x>1e-9]
    exact_a=[[rows[i][j] for i in support] for j in range(dim)]
    exact_a.append([F(1)]*len(support))
    weights=solve_exact(exact_a,[F(0)]*dim+[F(1)])
    assert all(x>=0 for x in weights)
    totals=[sum(w*rows[i][j] for i,w in zip(support,weights)) for j in range(dim+1)]
    assert all(x==0 for x in totals[:-1]) and totals[-1]>0
    return {"weights":[[i,str(w)] for i,w in zip(support,weights) if w],"positive_constant":str(totals[-1])}


def main():
    patterns,meta=collision_cases(make_values())
    out=Path(__file__).with_name("two_active_exact_certificates.jsonl.gz")
    remaining=[];count=0;certified=0;start=time.monotonic()
    with gzip.open(out,"wt") as f:
        header={"type":"header","metadata":meta,"pattern_count":len(patterns)}
        f.write(json.dumps(header,sort_keys=True)+"\n")
        for j,pattern in enumerate(patterns):
            r=pattern["residue"]
            assert abs(r.numerator)<149 and r.denominator<149
            for lift in range(r.denominator+1):
                for ks in product(range(3),repeat=3):
                    rows,labels,_=exact_system(pattern,meta["threshold"],lift,ks)
                    cert=certificate(rows)
                    entry={"type":"case","pattern_index":j,"residue":str(r),"lift":lift,"quotients":ks}
                    if cert is None:
                        entry["status"]="requires_hand_closure"
                        remaining.append({**entry,"basis":[[str(x) for x in row] for row in pattern["basis"]],
                                          "classes":pattern["classes"]})
                    else:
                        entry["status"]="exact_farkas";entry.update(cert);certified+=1
                    f.write(json.dumps(entry,sort_keys=True)+"\n");count+=1
            f.flush()
            if (j+1)%10==0:
                print(json.dumps({"patterns":j+1,"cases":count,"certificates":certified,
                                  "hand_closures":len(remaining),"seconds":round(time.monotonic()-start,1)}),flush=True)
    report={"status":"exact rational certificates generated and checked individually; independent replay pending",
            "metadata":meta,"pattern_count":len(patterns),"case_count":count,
            "certificate_count":certified,"remaining":remaining}
    Path(__file__).with_name("two_active_exact_report.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"cases":count,"exact_certificates":certified,"hand_closures":len(remaining),
                      "certificate_bytes":out.stat().st_size}),flush=True)


if __name__=="__main__": main()
