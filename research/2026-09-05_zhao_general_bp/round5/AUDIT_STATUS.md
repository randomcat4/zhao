# Round 5 audit status

Date: 2026-09-07

This directory contains **working mathematical notes**, not an independently audited theorem package.

## Current repository status

The authoritative thread status remains `../THREAD_STATUS.md`. In particular:

```text
general B_p is not proved,
no p>=7 counterexample has been certified,
the conditional {3p,4p-4} branch is not yet closed.
```

Round 5 should not alter that status until its symbolic arguments are independently checked.

## Material worth retaining

`ROUND5_WORKING_NOTES.md` records:

- the exact two-value actual-fibre congruence;
- the carefully scoped cross-atom `lambda`-difference / square-sum lemma;
- the maximum-support reduction candidate to external multiplicity types `1^(p-1)` and `2*1^(p-3)`;
- the fixed-`2g` reflection structure for the unique-double-value case;
- the exchange-component `(p-3)`-design as the correct global carrier for all-new squarefree exchanges;
- the label-sensitive `(p-3)`-link constraint to be used in the next additive-energy round;
- explicit retractions of two previously explored invalid deductions.

## Mandatory checks before promotion

Before moving any Round-5 claim into `THREAD_STATUS.md`, independently verify:

1. Every two-for-two exchange is positional and preserves the fixed complement sum.
2. Every invocation of maximum support distinguishes old values from genuinely new value classes.
3. Every use of

   ```text
   sum d_x^2 = 0 (mod p)
   ```

   verifies that all changed value classes are represented in the common external part on both sides.
4. The claimed deconvolution producing `a+b=2g` for an external value of multiplicity at least three is checked directly from the archived actual-sum fibre moments.
5. The two-double-value exclusion checks separately the cases `a=b`, `a!=b`, and overlaps with `g,h`.
6. Any affine-line capacity argument is positional and does not silently identify equal values with equal positions.
7. The exchange-component design proof checks the Boolean-polynomial degree bound and the `|X|=2p-3` borderline case independently.
8. No finite computation is used as a substitute for the all-prime quantifier.

## Retracted statements

Do not revive these without a new proof:

- a fixed long-representation family covers every `(b-1)`-subset;
- `Z_{3p} >= p*2^(p-3)+1` or `Z_{4p-4} >= p*2^(p-3)` from that covering claim;
- the unrestricted use of the square-sum exchange identity for completely disappearing/appearing squarefree value classes.

## Next audit target

The next round should focus only on the remaining near-squarefree configurations:

```text
squarefree rank 3 with no coloop / binary cocircuit,
squarefree rank 4,
unique-double-value rank 4,
p=7.
```

The preferred route is an exact positional energy/collision/capacity double count over all external two-sums, using the `(p-3)` link divisibility together with `ell_R`, `lambda_T`, and maximum-support exchange constraints.
