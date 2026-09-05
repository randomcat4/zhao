# Squarefree L15 elimination — proof and independent verification

This package archives the 2026-09-05 closure of the frozen squarefree branch L15.

Frozen branch: `S` is a 21-element subset of `F_5^4`, has no nonempty zero-sum subset of length 1 through 13, `s = sigma(S) != 0`, and the **complete** seven-subset fibre

`C = {B subset [21] : |B| = 7, sigma(B) = s}`

has exactly 15 blocks with every position in exactly 5 blocks. The result archived here is:

`L15_ELIMINATED_AND_AUDITED`.

The load-bearing proof is the hand argument in `PROOF.md`. Its endgame keeps the complete 4/5/6/7-subset fibres, derives the pair congruence `lambda_7(x,y) = lambda_4(x,y) (mod 5)`, proves `lambda_4(x,y) <= 4` from squarefreeness and the absence of short zero sums, and obtains the final mod-4 contradiction from equal incidence-row classes.

`INDEPENDENT_VERIFICATION.md` is a separate re-derivation and computational audit. The independent programs under `independent/src/` do not import the candidate generator. They check the finite arithmetic interface, independently recompute the labelled-point unordered simple 7-uniform 5-regular 15-edge hypergraph denominator, and run a third Gray-code full-subset audit of the retained false model.

This package does **not** claim the full 21-element squarefree endpoint A. It closes only L15. In the existing squarefree reduction, larger complete seven-fibre counts remain to be handled. It also does not upgrade the rescued B proof beyond that proof's separately stated dependency/audit level.

## Reproduce

```bash
python3 independent/src/proof_arithmetic_check.py > /tmp/l15-proof-arithmetic.json
python3 independent/src/independent_count.py > /tmp/l15-independent-count.json
python3 independent/src/gray_model_check.py proof/sources/known_false_model.json > /tmp/l15-gray-model.json
sha256sum -c SHA256SUMS.txt
```

Recorded association-structure denominator:

`860662922414727068051994283870582495183777624400448`.

The archived false model is deliberately not a counterexample: its complete seven-subset fibre has 238 blocks and it has many zero-sum subsets of length at most 13.

Verification level: independent audit within this research exchange; not external institutional or proof-assistant certification.
