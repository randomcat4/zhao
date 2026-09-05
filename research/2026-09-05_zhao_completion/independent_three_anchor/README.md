# Three-anchor theorem — independent audit

Status: **PROVED_AND_AUDITED** for the frozen three-anchor target only.

## Frozen target

Let `S` be a 21-position sequence in `F_5^4`. If some actual value `a` occurs **exactly three times**, then `S` contains a nonempty zero-sum subsequence of length at most 13. Other actual-value multiplicities are unrestricted. All subsequences are counted by positions. The proof never translates `a` to zero; it only quotients by the linear subgroup `<a>` after proving `a != 0`.

This closes every A multiplicity cell having at least one exactly-triple value, including the old two-triple and three-triple routes. It does **not** claim the full A endpoint for sequences with no exactly-triple value.

## Files

- `PROOF.md` — self-contained analytic proof.
- `AUDIT.md` — independent mathematical re-derivation of the load-bearing identities and endgame.
- `independent_check.py` — third-path deterministic finite-interface checker; it is self-contained and uses only the Python standard library.
- `independent_report.json` — machine-readable output from that checker.
- `independent_run.log` — exact terminal output and resource line from the independent run.
- `SHA256SUMS.txt` — hashes of the other files in this directory.

The earlier archived reproducibility bundle was also replayed during the audit, but the files committed here are sufficient to rerun the independent finite-interface checker and to inspect the analytic proof without that bundle.

## Load-bearing chain audited

1. For `n=4d+1`, the augmentation-ideal argument gives `1 + sum_j (-1)^j Z_j = 0 (mod 5)`; a Boolean-cube polynomial alternating sum independently gives the same identity.
2. Deleting one position of value `x` gives exactly
   `Z_(4d+1)=1_(x=s)` and `Z_(4d)=m(s-x)-1_(2x=s)`.
   Hence the half-value case is impossible, ordinary reflection pairs are fourfold, and the `d=3,4` auxiliary short-zero-sum bounds follow.
3. Fifteen nonzero quotient labels in `F_5^3` contain a 3-to-11-position zero sum; both the position graph proof and a reverse-value-class proof were checked, including repeated labels.
4. Writing `S=a^3 dot-union R`, every quotient-zero nonempty `Q subset R` with `|Q|<=10` has actual sum exactly `a`; the five coefficients `c in F_5` were checked against the availability of exactly three anchor positions.
5. An actual 14- or 15-position zero sum in `R` splits in the quotient so that one block can be replaced by one external anchor, yielding a nonempty actual zero sum of length at most 13.

No B-endpoint equality, two-dimensional occupancy bound, three-dimensional occupancy bound, or historical finite classification is load-bearing for this theorem.

## Independent finite-interface run

The self-contained checker recorded:

```text
INDEPENDENT_AUDIT: PASS
signed_identity_subsets=1769472
deletion_actual_rows=11232
graphs_n7=2097152; counterexamples=0
partitions=385
hard_core_anchors=620; maximum_min_zero=10
random_trials=2500; maximum_min_zero=10
report_sha256=a425544135fbd6e430e92df3e5755c68545e3ae81be1a9576398b611066fd5e8
```

The hard-core and fixed-seed searches are red-team checks only; the universal theorem is analytic.

## Reproduction

From this directory, with Python 3.10+ and no third-party packages:

```bash
python3 independent_check.py
```

Expected first line:

```text
INDEPENDENT_AUDIT: PASS
```

The analytic proof should be reviewed separately from the finite checker. The checker is an interface audit and adversarial cross-check, not a brute-force proof of all 21-position sequences.
