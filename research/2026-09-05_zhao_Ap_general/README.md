# General-prime endpoint A_p: low-multiplicity research thread

Collected: 2026-09-05; round 5 appended 2026-09-06; round 6 appended 2026-09-07.

## Target

For every prime `p >= 5`, prove or refute

\[
A_p:\qquad s_{\le 3p-2}(C_p^4)\le 5p-4.
\]

This directory archives six successive research rounds from one thread. It does **not** claim that the full endpoint is solved. The certified `p=5` endpoint under `research/2026-09-05_zhao_completion/` remains frozen.

## Strongest unconditional result in this thread

Any hypothetical counterexample to `A_p` satisfies

\[
\boxed{h(S)\le p-4.}
\]

No `h(S)<=p-5` theorem is currently certified.

## Reusable results

Rounds 1--4 archive:

- general deletion identities and actual-sum moment identities;
- parameterized projective double counting on `PG(3,p)`;
- correction-aware handling of `D_eq`, `D_col`, and `A_ap`;
- one-missing-value line-core and stronger line-occupancy control;
- the general `p-r` deletion normal form;
- the `p-4` residue family
  \[
  (x_0,x_1,x_2,x_3,x_4)
  \equiv(1+\theta,4\theta,6\theta,4\theta,\theta)\pmod p;
  \]
- in the hard `x_0=0, theta=-1` branch, the integer lower bounds
  \[
  x_1+x_2+x_3+x_4\ge6p-15,
  \]
  and for `p=7`, at least `48`;
- conditional `3p`-atom fixed-sum four-block structure and transversal restrictions.

Round 5 adds conditional `x_0>0` transversal reductions:

- all `K_{2,2}` configurations excluded for `p>=7`;
- induced `2K_2` excluded for `p>=17`;
- `P_4` excluded for `p>=29`;
- for `p>=29`, every nonempty transversal graph is a star with at most three leaves;
- for `p>=149`, only `K_{1,2}` or `K_{1,3}` remain as nontrivial components;
- an explicit actual `x_0=0, theta=-1` family satisfying point/pair/vector/deletion identities exists at height `p-1`; it is not an `A_p` counterexample.

Round 6 is a correction plus a new general mechanism:

- the continuation shortcut
  \[
  \theta=-1\Rightarrow\sigma(R)=0
  \]
  is **retracted**;
- the exact error is
  \[
  \Lambda_i=1-Z_{3p}(S\setminus r_i)\equiv0\pmod p,
  \]
  not `1`; therefore point weights do not force the unweighted total sum;
- augmented coordinates, top-degree sign, `Lambda_i=W_i`, and the derivative identity survive the audit;
- for general `p-r`, the first `r-3` over-deletion residues
  \[
  F_r,\ldots,F_{2r-4}
  \]
  form an integer-unimodular transform of the free parameters
  \[
  \theta_0,\ldots,\theta_{r-4};
  \]
- in the genuine `h=p-4, x_0=0` branch, `F_4=1`, hence some four-position complement `U` has
  \[
  |U|=4p-4,
  \qquad
  \prod_{u\in U}(1-X^u)\ne0;
  \]
- such a `U` is a disjoint union of `p-1` four-element bases, and its signed subset-sum coefficient function is a nonzero constant, so every group element occurs as a signed-count-supported subset sum;
- for `p>=11`, this `U` also satisfies `sigma(U) notin <a>`;
- the conditional `r=5` module is recorded but must not be used until `h=p-4` is actually closed.

## Current frontier

The complete `h=p-4` branch remains open. The main unresolved mechanisms are:

1. genuine-height `x_0=0 / theta=-1`: use the round-6 complement `U` and obtain **length-controlled** subset-sum representations, not merely existence of a representation;
2. conditional `x_0>0`: finish the remaining star-shaped fixed-sum four-block terminal structures (`K_{1,2}` and all-distinct `K_{1,3}` for large primes);
3. smaller primes where a two-point transversal is not forced.

The immediate `x_0=0` target is to refine

\[
\prod_{u\in U}(1-zX^u)
\]

by subset-size residue modulo `p`, or exploit the `p-1` basis decomposition, and combine a controlled representation with the four-point complement `R\setminus U` and the `p-4` anchors to produce an actual zero-sum of length at most `3p-2`.

## Files and reproduction

Each `roundN/` directory contains its research note and verifier material. Round 2 also contains `symbolic_interfaces.json`.

Run:

```bash
python3 round1/verify.py
python3 round2/verify_round2.py
python3 round3/verify_round3.py
python3 round4/verify_round4.py
python3 round5/verify.py
python3 round6/verify.py
```

The scripts check finite arithmetic/interfaces and explicit constructions. They are not exhaustive searches over all sequences in `F_p^4`; universal mathematical claims rest on the hand proofs in the notes.

## Upstream dependencies

Read together with:

- `WEB_START_HERE.md`
- `research/2026-09-04_zhao_exact/proofs/rank4_three_values.md`
- `research/2026-09-05_zhao_completion/fresh_audit/HARVEST_VERDICT.md`
- `research/2026-09-05_zhao_completion/independent_three_anchor/PROOF.md`
- `research/2026-09-05_zhao_completion/pro_round2/03_double_only/proof/proof_zh.md`
- `research/2026-09-05_zhao_completion/harvested_chat/squarefree_projection_proof.md`
