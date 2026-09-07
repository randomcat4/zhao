# General-prime endpoint A_p: low-multiplicity research thread

Collected: 2026-09-05; round 5 appended 2026-09-06.

## Target

For every prime `p >= 5`, prove or refute

\[
A_p:\qquad s_{\le 3p-2}(C_p^4)\le 5p-4.
\]

This directory archives five successive research rounds from one thread. It does **not** claim that the full endpoint is solved. The certified `p=5` endpoint under `research/2026-09-05_zhao_completion/` remains frozen.

## Strongest unconditional result in this thread

Any hypothetical counterexample to `A_p` satisfies

\[
\boxed{h(S)\le p-4.}
\]

The proof first excludes multiplicity `p-2`, then excludes multiplicity `p-3` for all primes. No counterexample family is claimed.

## Other reusable results archived here

- general deletion identities and actual-sum moment identities;
- parameterized projective double counting on `PG(3,p)`;
- a correction-aware cone for `D_eq`, `D_col`, `A_ap`;
- a one-missing-value line-core lemma and improved line-occupancy control;
- the general `p-r` deletion normal form;
- for the `p-4` branch,
  \[
  (x_0,x_1,x_2,x_3,x_4)
  \equiv(1+\theta,4\theta,6\theta,4\theta,\theta)\pmod p;
  \]
- if `x_0=0` in the hard `theta=-1` branch, the integer lift
  \[
  x_1+x_2+x_3+x_4\ge6p-15,
  \]
  and a separate `p=7` positive-weight certificate giving at least `48`;
- conditional `3p`-atom structure via a complete fixed-sum 4-uniform family with
  \[
  f\equiv0,\qquad f_i\equiv(p+1)/2\pmod p,
  \]
  full coverage and no common point;
- exclusion of the three-point double-hitting core for all `p >= 7`;
- round 4 large-prime transversal/fibre restrictions;
- round 5 exclusion of every `K_{2,2}` transversal configuration for all `p>=7`, induced `2K_2` for `p>=17`, and `P_4` for `p>=29`;
- consequently, for `p>=29` any nonempty transversal graph is a star with at most three leaves; for `p>=149` only `K_{1,2}` or `K_{1,3}` can remain, and the `K_{1,3}` case has four distinct singleton endpoint values;
- round 5 also gives an actual `x_0=0`, `theta=-1` sequence family satisfying the point/pair/vector identities, but only at height `p-1`; it is explicitly **not** an `A_p` counterexample.

## Current frontier

The complete `h=p-4` branch remains open. The main unresolved mechanisms are now:

1. the genuine-height `x_0=0` / `theta=-1` branch, where the scalar deletion system and the currently available point/pair integer lifts do not yet contradict `h=p-4`;
2. if a `3p` atom exists, the remaining star-shaped fixed-sum 4-uniform transversal structures, especially `K_{1,2}` and the all-distinct `K_{1,3}` branch;
3. smaller primes where a two-point transversal is not forced by the large-prime covering argument.

For `p >= 149`, a conditional `3p`-atom family has a transversal graph whose unique nontrivial component is `K_{1,2}` or `K_{1,3}`. This is a strict narrowing, not yet a contradiction.

## Files and reproduction

Each `roundN/` directory contains the complete research note, verifier source and the recorded verifier report. Round 2 also contains the auxiliary `symbolic_interfaces.json` required by its verifier.

Run:

```bash
python3 round1/verify.py
python3 round2/verify_round2.py
python3 round3/verify_round3.py
python3 round4/verify_round4.py
python3 round5/verify.py
```

The first four verifier entry points were replayed successfully when the original archive was prepared. Round 5 was run independently before being appended and records its output in `round5/verification_report.json`. These scripts check finite arithmetic/interfaces and explicit constructions; they are not exhaustive searches over all sequences in `F_p^4`, and universal results rest on the hand proofs in the notes.

## Upstream dependencies

Read together with:

- `WEB_START_HERE.md`
- `research/2026-09-04_zhao_exact/proofs/rank4_three_values.md`
- `research/2026-09-05_zhao_completion/fresh_audit/HARVEST_VERDICT.md`
- `research/2026-09-05_zhao_completion/independent_three_anchor/PROOF.md`
- `research/2026-09-05_zhao_completion/pro_round2/03_double_only/proof/proof_zh.md`
- `research/2026-09-05_zhao_completion/harvested_chat/squarefree_projection_proof.md`
