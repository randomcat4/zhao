"""Generic M=1 two-active-cover scalar relaxation; not an A_p proof."""
from itertools import combinations, permutations
from pathlib import Path
import json
import gzip
import time
import probe_double_star as core

core.DEG = {"x": (0, 7), "u": (-1, -1), "t": (1, 2),
            "v": (0, -1), "z": (0, -1), "h": (0, -1)}
core.MASS = {"x": (0, 2), "u": (0, 2), "t": (0, 2),
             "v": (0, -3), "z": (1, 0), "h": (-1, -3)}


def main():
    root = Path(__file__).parent
    results, survivors = {}, []
    start = time.monotonic()
    for size in range(6):
        for extra in combinations(["u", "t", "v", "z", "h"], size):
            names = ("x",)+extra
            count, maxbad = 0, 0
            classes = {}
            for n in range(len(names), 18):
                for indices in permutations(range(n), len(names)):
                    pos = dict(zip(names, indices))
                    for loop in [False, True]:
                        eq, seq = core.equations(n, pos, loop)
                        parameters, bad = core.classify(eq)
                        count += 1
                        maxbad = max(maxbad, bad)
                        if parameters is not None:
                            survivors.append({"n": n, "positions": pos, "loop": loop,
                                              "parameters": parameters, "multiplicity_forms": seq})
                            label = parameters[0]
                            classes[label] = classes.get(label, 0)+1
            results["".join(names)] = {"arrangements": count, "residual_bound": maxbad,
                                       "parameter_counts": classes}
            print("".join(names), count, classes, "residual",maxbad,flush=True)
            (root/"M1_generic_scalar_probe.json").write_text(json.dumps(results, indent=2)+"\n")
            data = (json.dumps(survivors, separators=(",", ":"))+"\n").encode()
            (root/"M1_generic_survivors.json.gz").write_bytes(gzip.compress(data, mtime=0))
    print("seconds", time.monotonic()-start,"survivors",len(survivors),flush=True)


if __name__ == "__main__":
    main()
