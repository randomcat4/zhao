"""Summarize the saved producer probe; no new extension or coloring search."""

from collections import Counter
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
source = BASE / "evidence/finite_two_triples_probe_cores.jsonl"
summary = json.loads((BASE / "evidence/finite_two_triples_probe.json").read_text(encoding="utf-8"))
assert hashlib.sha256(source.read_bytes()).hexdigest() == summary["certificate_sha256"]
rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()]
cores = [row for row in rows if row["type"] == "core_result"]
assert len(cores) == len({tuple(row["blocks"]) for row in cores}) == 8461
assert all(row["graph_completed"] for row in cores)
assert dict(sorted(Counter(row["candidate_count"] for row in cores).items())) == {
    int(k): v for k, v in summary["outside_candidate_count_distribution"].items()}

def subtotal(chosen):
    return {"cores": len(chosen),
            "six_subset_denominator": sum(row["six_subset_count"] for row in chosen),
            "seven_subset_denominator": sum(row["seven_subset_count"] for row in chosen),
            "candidate_count_distribution": dict(sorted(Counter(row["candidate_count"] for row in chosen).items())),
            "color_count_distribution": dict(sorted(Counter(row["number_of_colors"] for row in chosen).items()))}

residual = [row for row in cores if not row["no_six_new_singletons_certified_by_this_coloring"]]
assert [row["blocks"] for row in residual] == summary["unresolved_core_keys"]
maximum = max(row["candidate_count"] for row in cores)
result = {"status": "DESCRIPTIVE_TOTALS_ONLY_NOT_INDEPENDENT_CERTIFICATION",
          "all": subtotal(cores), "residual": subtotal(residual),
          "candidate_count_at_least_127": subtotal([row for row in cores if row["candidate_count"] >= 127]),
          "maximum_candidate_count": maximum,
          "maximum_candidate_cores": subtotal([row for row in cores if row["candidate_count"] == maximum]),
          "maximum_candidate_core_keys": [row["blocks"] for row in cores if row["candidate_count"] == maximum],
          "minimum_residual_blocks_lexicographic": min(row["blocks"] for row in residual),
          "source_sha256": summary["certificate_sha256"]}
(BASE / "evidence/finite_two_triples_totals.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: result[k] for k in ("residual", "maximum_candidate_count", "maximum_candidate_cores",
                                       "minimum_residual_blocks_lexicographic")}))
