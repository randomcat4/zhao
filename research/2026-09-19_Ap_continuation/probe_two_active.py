"""Necessary scalar-capacity relaxation; feasible output is NOT a sequence."""
import json
from pathlib import Path
from scipy.optimize import linprog


def check(p, m):
    rho, s = (p + 1) // 2, (p - 1) // 2
    n = rho + 2 - m
    # Twice the quotient linear-functional value, modulo p.
    scalar = {
        "t": -1, "u1": -2 - 2*m, "u2": 2*m - 7,
        "v1": 4*m - 3, "v2": 7 - 4*m,
        "r1": 2*m - 4, "r2": 1 - 2*m, "r3": -4,
        "n12": 3 - 6*m, "n13": -2 - 4*m,
        "n21": 6*m - 12, "n23": 4*m - 12,
    }
    scalar = {k: v % p for k, v in scalar.items()}
    labels = sorted(set(scalar.values()))
    ix = {z: i for i, z in enumerate(labels)}
    base = [0] * len(labels)
    for k, wt in {"t": s, "u1": m, "u2": n, "v1": s, "v2": s}.items():
        base[ix[scalar[k]]] += wt
    rows, rhs = [], []
    for keys, demand in [(["r1", "r2", "r3"], s),
                          (["n12", "n13"], (rho-m) % p),
                          (["n21", "n23"], (rho-n) % p)]:
        zs = {scalar[k] for k in keys}
        rows.append([-int(z in zs) for z in labels])
        rhs.append(-demand)
    result = linprog([1]*len(labels), A_ub=rows, b_ub=rhs,
                     bounds=[(x, None) for x in base], method="highs")
    assert result.success
    if result.fun <= 3*p-4 + 1e-7:
        collisions = {str(z): [k for k, v in scalar.items() if v == z] for z in labels}
        return {"m": m, "n": n, "relaxed_lower_bound": result.fun,
                "collisions": {z: k for z, k in collisions.items() if len(k) > 1}}
    return None


def main():
    all_results = []
    for p in [29, 47, 101, 149, 151, 157, 251, 503]:
        remaining = []
        rho = (p+1)//2
        for m in range(1, (rho+2)//2 + 1):
            n = rho + 2 - m
            if max(m, n) > p-4:
                continue
            r = check(p, m)
            if r is not None:
                remaining.append(r)
        all_results.append({"p": p, "remaining": remaining})
    out = {"status": "exploratory necessary-condition relaxation",
           "not_a_counterexample": True, "results": all_results}
    Path(__file__).with_name("two_active_scalar_probe.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(all_results, indent=2))


if __name__ == "__main__":
    main()
