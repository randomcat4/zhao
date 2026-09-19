"""Pure-standard-library exact catalogue and affine inequality model.

Shared mathematical model for deterministic certificate replay; no optimizer.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd
from pathlib import Path
import json
import time


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


