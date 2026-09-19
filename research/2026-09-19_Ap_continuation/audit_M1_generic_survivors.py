"""Exact capacity audit of the recorded M1 generic scalar candidates.

This does not certify that the generator has completed. The separate catalogue
verifier must establish completeness before a theorem is claimed.
"""
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import gzip
import json
from verify_double_star_survivors import residue_affine, add, neg, interval


def main():
    root = Path(__file__).parent
    records = json.loads(gzip.decompress((root/"M1_generic_survivors.json.gz").read_bytes()))
    remaining = []
    free_counts = Counter()
    base = Counter({(0,F(-1,2)):3,(0,F(1)):2,(0,F(2)):1,(0,F(-3,2)):1,
                    (1,F(0)):1,(-1,F(1,2)):1,(1,F(3)):1,(-1,F(-5,2)):1})
    mirror = Counter()
    for (a,c), count in base.items():
        mirror[-a,c-F(3,2)*a] += count
    fixed = 0
    for q in records:
        par = q["parameters"]
        if par[0] == "V_free":
            a,b,c = map(F,par[1:])
            tv,tc = -b/a,-c/a
            forms = Counter((aa*tv+bb,F(aa*tc+cc,2)) for aa,bb,cc in q["multiplicity_forms"])
            if any(forms[0,F(r)] for r in [0,-1,-2,-3]):
                free_counts["zero_or_height_violation"] += 1
            elif set(q["positions"]) in [{"x","u","v","z"},{"x","u","z"}] and all(forms[k]>=v-int(k==(0,F(-3,2)) and "v" not in q["positions"]) for k,v in base.items()):
                free_counts["mandatory_mass_ge_3p_plus5"] += 1
            elif set(q["positions"]) in [{"x","t","v","h"},{"x","t","h"}] and all(forms[k]>=v-int(k==(0,F(-3,2)) and "v" not in q["positions"]) for k,v in mirror.items()):
                free_counts["mandatory_mass_ge_3p_plus5"] += 1
            else:
                remaining.append({"unclosed_free":q})
            continue
        V,T = map(F,par)
        fixed += 1
        for mod in [1,3]:
            N,H = residue_affine(V/2,mod),residue_affine((-3-V)/2,mod)
            known = {"x":(F(0),F(1)),"u":(F(0),F(1)),"t":(F(0),F(1)),
                     "v":(F(1,2),F(-3,2)),"z":N,"h":H}
            masses = [residue_affine((a*T+b*V+c)/2,mod) for a,b,c in q["multiplicity_forms"]]
            conditions = [add(N,neg(H)),add(H,(0,-1)),add((1,-4),neg(N))]
            for m in masses:
                conditions += [add(m,(0,-1)),add((1,-4),neg(m))]
            total = add(*masses,*(v for name,v in known.items() if name not in q["positions"]))
            conditions += [add((3,-3),neg(total))]
            possible = interval(conditions)
            if possible:
                remaining.append({"V":str(V),"T":str(T),"n":q["n"],"positions":q["positions"],
                                  "loop":q["loop"],"mod4":mod,
                                  "p_interval":[str(x) for x in possible],"forms":q["multiplicity_forms"]})
    report = {"status":"OPEN" if remaining else "PASS_ON_RECORDED_CATALOGUE",
              "recorded_cases":len(records),"fixed_cases":fixed,"free_case_dispositions":dict(free_counts),
              "remaining":remaining,
              "scope":"Exact all-prime capacity necessary conditions, conditional on catalogue completeness. N>=H is chosen by swapping the isolated-edge endpoints."}
    (root/"M1_generic_survivor_audit.json").write_text(json.dumps(report,indent=2)+"\n")
    print({k:v for k,v in report.items() if k!='remaining'})
    print('remaining',len(remaining),Counter((''.join(sorted(q.get('positions',{}))),q.get('V'),q.get('mod4')) for q in remaining))


if __name__ == "__main__":
    main()
