"""Explore exact critical-value collision patterns, then LP necessary conditions.

The LP treats p as a real parameter >= threshold. It is a relaxation only.
No feasible pattern is a zero-sum sequence or a counterexample.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd
from pathlib import Path
import json
import time
from scipy.optimize import linprog


def rref(rows):
    rows = [list(map(F, row)) for row in rows if any(row)]
    i = 0
    for j in range(4):
        pivot = next((k for k in range(i, len(rows)) if rows[k][j]), None)
        if pivot is None:
            continue
        rows[i], rows[pivot] = rows[pivot], rows[i]
        lead = rows[i][j]
        rows[i] = [x/lead for x in rows[i]]
        for k in range(len(rows)):
            if k != i and rows[k][j]:
                mul = rows[k][j]
                rows[k] = [x-mul*y for x, y in zip(rows[k], rows[i])]
        i += 1
        if i == len(rows):
            break
    return tuple(tuple(row) for row in rows[:i])


def reduce_vec(v, basis):
    v = list(map(F, v))
    for row in basis:
        j = next(j for j, x in enumerate(row) if x)
        mul = v[j]
        v = [x-mul*y for x, y in zip(v, row)]
    return tuple(v)


def primitive(v):
    d = 0
    for x in v:
        d = gcd(d, abs(x))
    v = tuple(x//d for x in v)
    return v if next(x for x in v if x) > 0 else tuple(-x for x in v)


def largest_prime_factor(n):
    n = abs(n)
    best = 1
    d = 2
    while d*d <= n:
        while n%d == 0:
            best, n = d, n//d
        d += 1
    return max(best, n)


def make_values():
    e = [tuple(int(i == j) for j in range(4)) for i in range(4)]
    def lin(*terms):
        return tuple(sum(k*v[j] for k, v in terms) for j in range(4))
    b = (1, 1, 1, 0)
    vals = {"y": (0,0,0,0), "t": e[3]}
    for i in range(3):
        vals[f"b{i+1}"] = e[i]
        vals[f"u{i+1}"] = lin((1,e[i]), (1,e[3]))
        vals[f"v{i+1}"] = lin((1,b), (-2,e[i]))
        vals[f"r{i+1}"] = lin((1,b), (-1,e[i]))
    for i in [0,1]:
        for j in range(3):
            if i != j:
                vals[f"n{i+1}{j+1}"] = lin((1,e[3]), (2,e[i]), (-1,e[j]))
    return vals


def collision_cases(vals):
    diffs = set()
    raw_norm2 = 0
    for a, b in combinations(vals.values(), 2):
        d = tuple(x-y for x, y in zip(a,b))
        raw_norm2 = max(raw_norm2, sum(x*x for x in d))
        diffs.add(primitive(d))
    cand, permanent = set(), []
    for d in sorted(diffs):
        slope = -2*d[0] + 2*d[1]
        const = -d[0] - 6*d[1] - d[2] - 4*d[3]
        if slope:
            cand.add(F(-const, slope))
        elif const == 0:
            permanent.append(d)
    exceptions = []
    for a,b in combinations(cand, 2):
        determinant = a.numerator*b.denominator-b.numerator*a.denominator
        exceptions.append(largest_prime_factor(determinant))
    threshold = max(149, max(exceptions, default=1)+1)
    patterns = []
    fixed_positive = {"t", "u1", "u2", "v1", "v2"}
    cores = {"y", "b1", "b2", "b3"}
    zero = {"u3", "v3"}
    for m in sorted(cand):
        eligible = []
        for d in sorted(diffs):
            if (-2*d[0]+2*d[1])*m -d[0]-6*d[1]-d[2]-4*d[3] == 0:
                eligible.append(d)
        bases = {()}
        bases.update(rref([d]) for d in eligible)
        bases.update(rref([a,b]) for a,b in combinations(eligible, 2))
        seen = set()
        for basis in sorted(bases):
            groups = {}
            for name,v in vals.items():
                groups.setdefault(reduce_vec(v,basis), []).append(name)
            classes = tuple(sorted(tuple(sorted(g)) for g in groups.values()))
            if classes in seen:
                continue
            seen.add(classes)
            bad = False
            for g in classes:
                g = set(g)
                if len(g & cores) > 1 or len(g & fixed_positive) > 1:
                    bad = True
                if g & fixed_positive and g & (cores | zero):
                    bad = True
            if not bad:
                patterns.append({"residue": m, "basis": basis, "classes": classes})
    return patterns, {"threshold": threshold, "critical_residue_count": len(cand),
                      "max_exception_prime": max(exceptions, default=1),
                      "maximum_raw_difference_norm_squared": raw_norm2,
                      "permanent_difference_count": len(permanent)}


def feasible(pattern, threshold, lift, quotients):
    r = pattern["residue"]
    d,c = r.denominator,r.numerator
    # Every expression is represented as coefficients in (p, x_1,...,x_l, 1).
    groups = pattern["classes"]
    core = {"y","b1","b2","b3","u3","v3"}
    fixed = {"t": (F(1,2),F(-1,2)), "v1": (F(1,2),F(-1,2)),
             "v2": (F(1,2),F(-1,2)), "u1": (F(lift,d),F(c,d)),
             "u2": (F(1,2)-F(lift,d),F(5,2)-F(c,d))}
    unknown = [g for g in groups if not (set(g)&(core | set(fixed)))]
    dim = 1+len(unknown)
    zero = [F(0)]*(dim+1)
    value = {}
    for g in groups:
        v = zero.copy()
        if set(g)&core:
            pass
        elif set(g)&set(fixed):
            a,b = fixed[next(x for x in g if x in fixed)]
            v[0],v[-1] = a,b
        else:
            v[1+unknown.index(g)] = 1
        for name in g:
            value[name] = v
    ub, rhs, eq, erhs = [],[],[],[]
    def inequality(v):
        ub.append([float(x) for x in v[:-1]])
        rhs.append(float(-v[-1]))
    def combine(items):
        return [sum(a*v[i] for a,v in items) for i in range(dim+1)]
    # Bounds for every named class; all unlisted positions remain free.
    for g in groups:
        v = value[g[0]]
        cap = v.copy(); cap[0] -= 1; cap[-1] += 4
        inequality(cap)
    for key in ["u1","u2"]:
        v = [-x for x in value[key]]; v[-1] += 1
        inequality(v)
    inequality(combine([(1,value["u1"]),(-1,value["u2"])]))
    total = combine([(1,value[g[0]]) for g in groups])
    total[0] -= 3; total[-1] += 4
    inequality(total)
    class_id = {x:i for i,g in enumerate(groups) for x in g}
    for pos, partners, extra, k in [
        ("t",["r1","r2","r3"],1,quotients[0]),
        ("v1",["u1","n12","n13"],0,quotients[1]),
        ("v2",["u2","n21","n23"],0,quotients[2])]:
        v = combine([(1,value[x]) for x in partners])
        v[-1] += extra-sum(class_id[x] == class_id[pos] for x in partners)
        v[0] -= F(1,2)+k; v[-1] -= F(1,2)
        eq.append([float(x) for x in v[:-1]]); erhs.append(float(-v[-1]))
    result = linprog([1]+[0]*(dim-1), A_ub=ub,b_ub=rhs,A_eq=eq,b_eq=erhs,
                     bounds=[(threshold,None)]+[(0,None)]*(dim-1),method="highs")
    if result.success:
        return {"lift": lift,"degree_quotients":quotients,"minimum_relaxed_p":float(result.x[0]),
                "unknown_values":{str(g):float(result.x[1+i]) for i,g in enumerate(unknown)}}
    if result.status != 2:
        raise RuntimeError(result.message)
    return None


def main():
    vals = make_values()
    patterns, meta = collision_cases(vals)
    print(json.dumps({**meta,"patterns_after_distinctness":len(patterns)}),flush=True)
    results = []
    tested = 0
    start = time.monotonic()
    for j,pattern in enumerate(patterns):
        r = pattern["residue"]
        hits = []
        for lift in range(-1,r.denominator+2):
            # At p>=149, these coarse bounds exclude irrelevant lifts safely.
            if F(lift,r.denominator) < 0 or F(lift,r.denominator) > F(1,2):
                continue
            for ks in product(range(3), repeat=3):
                tested += 1
                v = feasible(pattern,meta["threshold"],lift,ks)
                if v is not None:
                    hits.append(v)
        if hits:
            results.append({"residue":str(r),"basis":[[str(x) for x in row] for row in pattern["basis"]],
                            "classes":pattern["classes"],"feasible_relaxations":hits})
        if (j+1)%50 == 0:
            print(json.dumps({"patterns_checked":j+1,"LPs_checked":tested,"remaining_patterns":len(results),
                              "elapsed_seconds":round(time.monotonic()-start,2)}),flush=True)
    report = {"status":"Exploratory LP necessary conditions; not a sequence classification theorem",
              "metadata":meta,"patterns_checked":len(patterns),"LPs_checked":tested,
              "remaining_patterns":results}
    Path(__file__).with_name("two_active_collision_classification.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"LPs_checked":tested,"remaining_patterns":len(results),
                      "remaining_residues":sorted(set(r["residue"] for r in results))}),flush=True)


if __name__ == "__main__":
    main()
