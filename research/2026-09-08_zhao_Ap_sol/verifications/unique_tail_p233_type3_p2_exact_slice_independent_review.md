# `p=233`, type `(3)`, `|P|=2` exact-slice independent review

STATUS: **CORRECT**

Date: 2026-09-09

## Frozen inputs

This verdict is bound to exactly the following author artifacts:

- `unique_tail_p233_type3_p2_exact_slice.py`
  SHA-256 `22631e977e14b12e4e8d1cbd18e7cde0c7c81d7b3989364f0d66e616ce3371f1`
- `unique_tail_p233_type3_p2_exact_slice_report.json`
  SHA-256 `440b9fecb57e66b018bab44b37f87e97e68cb03155f71e7ddb8d9c76f975281a`
- `proofs/unique_tail_p233_type3_p2_exact_slice.md`
  SHA-256 `30ce9d66a91d0e47c22b5731b66b450e9cc9155c872e60d482154dc6e8c6f274`

The certified rank-one-reduction dependency is also recorded consistently in
the script, report, and proof with independent-review SHA-256
`8487137667255b49f74ce8a0fe79c2d12222e45d54776eb5c8458bce00aed5d1`.

## Schema verification

The instance parser fixes precisely

\[
p=233,\quad (\ell,b)=(7,4),\quad |U|=3,\quad
\text{packing type }(3),\quad |P|=2,\quad \kappa=1.
\]

It accepts one shared 474-row literal-position array `Y`.  `T`, `U`, all
selected endpoints, `L`, `R`, `P`, and `K` are subsets of that same index
universe.  The parser recomputes

\[
L=U\cup\bigcup H_i,\qquad R=Y\setminus L,\qquad K=R\setminus P,
\]

and each endpoint-specific

\[
Q_H=K\cup(L\setminus H)=Y\setminus(H\mathbin{\dot\cup}P).
\]

All selected endpoints have literal length seven.  Their nonempty proper
traces on `U` are pairwise distinct, all three singleton traces occur, and the
four supplied simple edges join trace-disjoint endpoints.  Every edge uses the
same literal nonaxial witness position and has nonzero projected intersection
sum.  The certified reduction is implemented as the exact rank-two test on
`rho(U)`.

The quotient and actual-axis equalities for `Y`, `U`, `T`, every endpoint, and
`P` were checked against the code.  They imply and the parser rechecks that
every `Q_H` has length `2p-1=465` and quotient sum `q`, while
`X_1 union U union P` is the automatic six-term `F2` block.  Multiplicity is
checked on actual four-coordinate labels after adjoining all `p-4=229` core
copies.

## Exact CEGAR interface

The eleven registered contracts jointly retain the required universal
obligations:

1. rho-zero-freeness of `K`;
2. rho-atomicity of every `Q_H`;
3. every mixed `P`/`Q_H` target, with one independent `P`-complement orbit but
   all literal `Q_H` subsets still quantified;
4. the complete quotient-zero spectrum in lengths one through eight;
5. the whole forbidden middle layer from 9 through `2p+2`;
6. uniqueness of the positive-core `F3` tail and anchoring of every `F3` tail
   on `U`;
7. the allowed-short-block intersection network and nonzero quotient sums of
   distinct `F3` intersections;
8. every nonempty proper internal subset of every induced `F3` complement;
9. every nonempty proper internal subset of the six-term `F2` extreme
   complement;
10. all zero-, one-, two-, and three-position Hasse congruences, including the
    fixed-core-position symmetry classes;
11. actual `C_233^4` atomicity of `Z=X^229 union Y`.

The Hasse row arithmetic independently recomputes to 17,976,380 congruences.
A bare asserted Hasse residual is deliberately rejected because the aggregate
oracle requires a complete short-star support/count certificate.

## Adversarial witness regression

The no-instance default self-audit completed successfully.  It reported 48
compressed-atom comparisons, five short-intersection classifier rows, eleven
oracle contracts, and the exact Hasse total above.  The emitted JSON matched
the checked-in report byte for byte, and report certificate
`05f913f2b8d1508cf09aacb42f56c4805550731c3fed3a0ef0b43f4d3e11a2db`
recomputed correctly.

Fresh end-to-end calls to `validate_violation_witness` gave:

| Adversarial case | Required result | Observed result |
|---|---:|---:|
| `F3` block plus its non-short full complement | reject | reject |
| disjoint allowed `F1` length 5 plus `F2` length 4 | verified violation | verified violation |
| disjoint positive-core `F2`/`F2` pair with enough literal core positions | verified violation | verified violation |
| otherwise valid pair with overlapping tail positions | reject | reject |
| distinct `F3` pair with quotient-zero feasible intersection | verified violation | verified violation |
| distinct `F3` pair with nonzero intersection quotient | reject | reject |
| identical `F3` block presented twice | reject | reject |
| bare Hasse residual | reject | reject |

The repaired helper first restricts both pair sides to the permitted short
spectrum.  Literal disjointness then requires disjoint tail positions and
`c_left+c_right <= p-4`, exactly the condition for choosing disjoint core
positions of the two requested cardinalities.  The separate `F3` intersection
branch checks both blocks, their distinctness, the full feasible interval for
the number of common core positions, and the quotient sum of that literal
intersection.

## Status boundary

No 474-position instance is loaded and no oracle has returned an exact `CLEAR`
certificate.  The report therefore correctly stops at

`INSTANCE_SCHEMA/CEGAR_ORACLES_UNINSTANTIATED/GLOBAL_INCOMPLETE`.

For a statically valid supplied instance it would still stop at
`RELAXED_STATIC_INSTANCE_ONLY/EXACT_ORACLES_PENDING/GLOBAL_INCOMPLETE` until
all eleven contracts were discharged.  Nothing in these artifacts claims
`SAT`, `UNSAT`, a counterexample to the endpoint, or the global theorem.

The proof's phrase “two small audits” precedes three displayed audit bullets;
this is a harmless editorial miscount.  The script and report unambiguously
record all three groups and their exact row counts, so it does not change the
interface or verdict.

## Verdict

The three frozen artifacts faithfully implement and document the requested
fixed-instance schema and exact CEGAR boundary.  The earlier intersection
witness false positive and length-nine false negative are repaired, and no
remaining critical gap or false universal claim was found.
