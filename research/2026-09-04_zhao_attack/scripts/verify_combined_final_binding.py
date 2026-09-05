"""Bind the final reviewed text. No search or mathematical tree is executed."""
from difflib import unified_diff
from hashlib import sha256
from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[1]
source = BASE / "proofs" / "certified_reduction.md"
old = BASE / "evidence" / "verify_combined_certified_reduction_snapshot.md"
snapshot = BASE / "evidence" / "verify_combined_certified_reduction_final_snapshot.md"
diff_path = BASE / "evidence" / "verify_combined_certified_reduction_final_diff.txt"
output = BASE / "evidence" / "verify_combined_final_binding.json"
old_bytes, final_bytes = old.read_bytes(), source.read_bytes()
old_text, final_text = old_bytes.decode("utf-8"), final_bytes.decode("utf-8")
assert sha256(old_bytes).hexdigest() == "ec64262b72048645f39e8c53ec2e7d6d153b76325c185ee2b27c9546d53f07a9"
for expected in (
    "3. a+b≤7。", "4. 若a≥2，则a+b≤6。",
    "| 0 | 7 | 14 | 13 |", "| 1 | 6 | 13 | 12 |",
    "| 2 | 4 | 13 | 12 |", "| 3 | 1 | 14 | 13 |",
    "所以A坏例至少13种元素，B坏例至少12种元素。",
    "第5步（只依赖第2步，不依赖本步）", "8709个四子集",
    "端点 A/B 仍未证明。", "K(C5^4)仍只被确定在{10,14,15}中",
):
    assert expected in final_text, expected
snapshot.write_bytes(final_bytes)
assert source.read_bytes() == snapshot.read_bytes() == final_bytes
diff_path.write_text("".join(unified_diff(old_text.splitlines(keepends=True),
                                         final_text.splitlines(keepends=True),
                                         fromfile=str(old.relative_to(BASE)),
                                         tofile=str(snapshot.relative_to(BASE)))), encoding="utf-8")
result = {
    "status": "CORRECT_FINAL_TEXT_BOUND",
    "source": str(source), "source_sha256": sha256(final_bytes).hexdigest(),
    "source_line_count": len(final_text.splitlines()),
    "snapshot": str(snapshot), "snapshot_sha256": sha256(snapshot.read_bytes()).hexdigest(),
    "previous_snapshot_sha256": sha256(old_bytes).hexdigest(),
    "diff": str(diff_path), "diff_sha256": sha256(diff_path.read_bytes()).hexdigest(),
    "review": "Final full text independently read; steps 3 and 4 match the already audited interfaces; forward reference to step 5 is noncircular under the global height input and step 2.",
    "scope": "Text identity and final statement only. No trees, Lean builds, or new local extensions rerun or incorporated.",
    "table": [{"a":a,"b_upper":b,"A_support_lower":21-2*a-b,"B_support_lower":20-2*a-b}
              for a,b in enumerate((7,6,4,1))],
    "endpoint_status": "A INCOMPLETE; B INCOMPLETE; K in {10,14,15}",
}
output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,ensure_ascii=False))
