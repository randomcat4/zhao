"""Audit every saved lazy-SAT cut directly as a zero-sum multiset."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
audits = []
for result_file in sorted((ROOT / "evidence").glob("search_sat_*.result.json")):
    result = json.loads(result_file.read_text(encoding="utf-8"))
    config = result["config"]
    cuts_file = result_file.with_name(result_file.name.replace(".result.json", ".cuts.jsonl"))
    histogram = {}
    count = 0
    seen = set()
    for line_number, line in enumerate(cuts_file.read_text(encoding="utf-8").splitlines(), 1):
        cut = json.loads(line)
        assert cut, (cuts_file.name, line_number, "empty cut")
        codes = [code for code, _ in cut]
        assert len(codes) == len(set(codes)), (cuts_file.name, line_number, "repeated code")
        assert all(1 <= code <= 624 and 1 <= multiplicity <= config["cap"] for code, multiplicity in cut)
        length = sum(multiplicity for _, multiplicity in cut)
        assert 1 <= length <= config["m"]
        coordinates = [[(code // (5**j)) % 5 for j in range(4)] for code, _ in cut]
        assert all(sum(v[j] * multiplicity for v, (_, multiplicity) in zip(coordinates, cut)) % 5 == 0 for j in range(4))
        if config["mode"] == "affine":
            assert all(sum(v) % 5 == 1 for v in coordinates)
        canonical = tuple(sorted(tuple(pair) for pair in cut))
        assert canonical not in seen, (cuts_file.name, line_number, "duplicate cut")
        seen.add(canonical)
        histogram[length] = histogram.get(length, 0) + 1
        count += 1
    assert count == result["cuts"]
    audit = dict(cuts_file=cuts_file.name, count=count, lengths=histogram, all_nonempty_zero_sums=True, all_within_cap_and_forbidden_length=True, all_distinct=True, sha256=hashlib.sha256(cuts_file.read_bytes()).hexdigest(), solver_status=result["status"], solver_reason=result["reason"])
    audits.append(audit)
    print(json.dumps(audit))
output = ROOT / "evidence" / "search_cut_audit.json"
output.write_text(json.dumps(audits, indent=2) + "\n", encoding="utf-8")
