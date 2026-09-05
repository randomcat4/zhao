"""Emit a kernel-checkable finite certificate only; not the whole H11 theorem."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
rows=json.loads((root/'h11_continue_scalar_egz_v2.json').read_text(encoding='utf8'))['certificates']
def natlist(xs):return '['+', '.join(map(str,xs))+']'
prefix='''import Std
set_option maxRecDepth 100000
set_option maxHeartbeats 200000000

namespace H11ScalarCertificate
structure Entry where
  n : List Nat
  k : List Nat
deriving DecidableEq, Repr

def entries : List Entry := [
'''
body=',\n'.join('  ⟨'+natlist(r['n'])+', '+natlist(r['k'])+'⟩' for r in rows)
suffix='''
]

def distributions : List (List Nat) :=
  (List.range 10).flatMap fun a =>
    (List.range (10-a)).flatMap fun b =>
      (List.range (10-a-b)).flatMap fun c =>
        (List.range (10-a-b-c)).map fun d => [a,b,c,d,9-a-b-c-d]

def isPartial (p : Nat × Nat) : Bool := (0 < p.2) && (p.2 < p.1)
def valid (e : Entry) : Bool :=
  let pairs := e.n.zip e.k
  let count := (pairs.filter isPartial).length
  let large := pairs.any fun p => isPartial p && (3 <= p.1)
  let residue := (((List.range 5).zip e.k).map fun p => p.1*p.2).sum % 5
  e.n.length == 5 && e.k.length == 5 && e.n.sum == 9 && e.k.sum == 5 &&
    pairs.all (fun p => p.2 <= p.1) &&
    ((residue == 0 && (large || 2 <= count)) ||
     (residue == 2 && 1 <= count))

theorem all_counts_covered : entries.map Entry.n = distributions := by decide
theorem all_selections_valid : entries.all valid = true := by decide
theorem number_of_counts : entries.length = 715 := by decide

#print axioms all_counts_covered
#print axioms all_selections_valid
#print axioms number_of_counts
end H11ScalarCertificate
'''
(root/'formal/H11ScalarCertificate.lean').write_text(prefix+body+suffix,encoding='utf8')
print('Wrote formal/H11ScalarCertificate.lean with',len(rows),'entries')
