"""Emit the 2365-row scalar table, not the whole star/H11 proof."""
from pathlib import Path
import json
root = Path(__file__).resolve().parents[1]
rows = json.loads((root/'evidence/root_continue_star_d2.json').read_text(encoding='utf8'))['scalar_certificates']
def ns(v): return '['+', '.join(map(str,v))+']'
prefix = '''import Std
set_option maxRecDepth 100000
set_option maxHeartbeats 200000000
namespace StarD2ScalarCertificate
structure Entry where
  n : List Nat
  k : List Nat
  repeatClass : Nat
  varyClass : Nat
deriving DecidableEq, Repr
def entries : List Entry := [
'''
body = ',\n'.join('  ⟨'+ns(r['n'])+', '+ns(r['k'])+', '+str(5 if r['repeat_class']==-1 else r['repeat_class'])+', '+str(r['vary_class'])+'⟩' for r in rows)
suffix = '''
]
def distributions : List (List Nat) :=
  (List.range 10).flatMap fun a =>
    (List.range (10-a)).flatMap fun b =>
      (List.range (10-a-b)).flatMap fun c =>
        (List.range (10-a-b-c)).map fun d => [a,b,c,d,9-a-b-c-d]
def patterns : List (List Nat × Nat) :=
  distributions.flatMap fun n =>
    (5 :: (List.range 5).filter (fun r => 2 <= n[r]!)).map (fun r => (n,r))
def valid (e : Entry) : Bool :=
  let residue := (((List.range 5).zip e.k).map fun p => p.1*p.2).sum % 5
  let c := e.varyClass
  e.n.length == 5 && e.k.length == 5 && e.n.sum == 9 && e.k.sum == 5 &&
    (e.n.zip e.k).all (fun p => p.2 <= p.1) &&
    (residue == 0 || residue == 2) && c < 5 &&
    0 < e.k[c]! && e.k[c]! < e.n[c]! &&
    (c != e.repeatClass || e.n[c]! != 2)
theorem all_patterns_covered : entries.map (fun e => (e.n,e.repeatClass)) = patterns := by decide
theorem all_selections_valid : entries.all valid = true := by decide
theorem number_of_patterns : entries.length = 2365 := by decide
#print axioms all_patterns_covered
#print axioms all_selections_valid
#print axioms number_of_patterns
end StarD2ScalarCertificate
'''
(root/'formal/StarD2ScalarCertificate.lean').write_text(prefix+body+suffix,encoding='utf8')
print('Wrote 2365-entry scalar certificate')
