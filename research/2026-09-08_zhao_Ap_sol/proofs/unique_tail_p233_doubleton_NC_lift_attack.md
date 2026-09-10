# Fixed Models N/C: unified lift and the first automatic-short boundary

## Status and quantifiers

This note restores the actual (C_{233}^4) labels only at a sharply stated
interface.

1. **Fixed Model N is UNSAT.**  For every actual lift having the displayed
   endpoint sums (3a) and the unique positive-core (F_3) tail, a second
   literal tail is forced.  This is a statement about the fixed Model N only.
2. **Fixed Model C is RELAXED SAT at the endpoint-internal/P-mixed layer.**
   There exists the explicit lift and the explicit two-position (P) below
   such that the first moments, both maximal (\rho)-atoms, the actual
   multiplicity bound, every (P)-mixed target fibre, and every
   (\rho)-zero subset internal to either displayed endpoint all pass.
3. The same Model-C witness is **not** SAT for the global automatic-short
   spectrum.  A literal bad length-three block is given below.  Therefore this
   note neither proves nor disproves the existence of a different globally
   short-compatible lift of fixed Model C.

All subsets below are subsets of literal positions, not merely subsets of
support values.

## 1. A two-line exclusion of fixed Model N

Write

\[
U=\{u_e,u_f,u_t\},\qquad
V=\{u_e,x_f,x_t\}.
\]

The three relevant Model-N endpoints have a common four-position part (C_N)
and are

\[
H_s=\{u_e,x_f,x_t\}\sqcup C_N,
\]
\[
H_{ef}=\{u_e,u_f,x_t\}\sqcup C_N,
\qquad
H_{et}=\{u_e,u_t,x_f\}\sqcup C_N.
\]

Every endpoint has actual sum (3a).  Equating the sums of (H_s) and
(H_{ef}), then cancelling their common literal positions, gives

\[
\gamma(x_f)=\gamma(u_f),
\]

and the same comparison of (H_s) with (H_{et}) gives

\[
\gamma(x_t)=\gamma(u_t).
\]

Consequently (sigma(V)=sigma(U)=3a-4x).  Hence

\[
\sigma(X_4\sqcup V)=3a.
\]

This is a length-seven positive-core (F_3) block.  But (V\ne U) as literal
position sets, so it is a second tail, contradicting uniqueness.  Notice that
the proof does not use (P), the labels on the common kernel, a cancellation
of a zero divisor, or Property B.  It also does not extend the conclusion to
any model other than this fixed Model N.

## 2. Fixed Model C and an explicit actual lift

Use coordinates

\[
\gamma(v)=(h(v),q(v),\rho(v))
   \in C_{233}\oplus C_{233}\oplus C_{233}^2,
\]

with (a=(1,0,0)), (x=(0,1,0)), and

\[
e=(1,0),\quad f=(0,1),\quad
g=t=-e-f=(-1,-1),\quad h=t-e=(-2,-1).
\]

The common kernel is

\[
K=g^{231}h^{231}.
\]

Put

\[
B_s=\{u_t,u_f,x_s\},\qquad
B_d=\{x_h,u_e,x_d\},
\]

and

\[
C_0=\{y,c_{e,1},c_{e,2},c_f\}.
\]

The two displayed endpoints and complements are

\[
H_e=B_d\sqcup C_0,\qquad H_{ft}=B_s\sqcup C_0,
\]

\[
Q_e=K\sqcup B_s,\qquad Q_{ft}=K\sqcup B_d.
\]

The local (\rho)-labels are

\[
\rho(x_s)=h+3g=(-5,-4),\quad
\rho(x_h)=h,\quad
\rho(x_d)=g+2h=(-5,-3),\quad
\rho(y)=4e+3f,
\]

with the names (u_e,u_f,u_t,c_{e,i},c_f) carrying the evident labels
(e,f,g,e,f).

Here is the full lift.  Entries are ((h,q,\rho)), and signed representatives
are used.

| Literal positions | Multiplicity | Actual label |
|---|---:|---|
| ordinary (K:g) | 229 | ((0,0,g)) |
| exceptional (K:g) | 1 | ((2,0,g)) |
| exceptional (K:g) | 1 | ((0,1,g)) |
| ordinary (K:h) | 229 | ((0,0,h)) |
| exceptional (K:h) | 1 | ((1,0,h)) |
| exceptional (K:h) | 1 | ((-7,0,h)) |
| (u_e,u_f,u_t) | one each | ((2,-1,e),(0,-3,f),(1,0,g)) |
| (x_s,x_h,x_d) | one each | ((1,3,h+3g),(0,1,h),(0,0,g+2h)) |
| (y) | 1 | ((0,0,4e+3f)) |
| (c_{e,1},c_{e,2},c_f) | one each | ((1,0,e),(1,0,e),(-1,0,f)) |
| (P_L,P_R) | one each | ((0,2,-g),(-1,1,g)) |

Direct summation gives

\[
\sigma(U)=(3,-4,0),\quad
\sigma(P)=(-1,3,0),\quad
\sigma(W)=(1,1,0),\quad
\sigma(Y)=(0,4,0),
\]

and, for both displayed endpoints,

\[
\sigma(H)=(3,0,0),\qquad
\sigma(Q_H)=(-2,1,0).
\]

Thus (X=x^{229}) and (Y=P\sqcup W) have total actual sum zero after they
are joined.  The only actual values of multiplicity 229 are (x), the
ordinary (g)-label, and the ordinary (h)-label; hence the required cap is
met exactly.

The script also enumerates the compressed (\rho)-count vectors in each
(Q_H).  For (Q_e) its only zero submultisets are

\[
(0,0,0,0),\qquad (1,1,231,232)
\]

on the four types (f,h+3g,h,g); for (Q_{ft}) they are

\[
(0,0,0,0),\qquad (1,1,232,231)
\]

on the four types (e,g+2h,h,g).  Hence both (Q_H) are literal maximal
minimal zero-sum sequences in the (\rho)-projection.

## 3. Complete endpoint-internal short closure

For every (\rho)-zero subset (S\subseteq H), a quotient-zero completion by
the (x)-core must use

\[
c=-q(S)\pmod {233},\qquad 0\le c\le229.
\]

The script enumerates all such literal subsets.  There are 18 rows including
the empty subset in each endpoint, hence 16 nonempty rows.  The nontrivial
proper rows reduce to the following complementary pairs; (i=1,2).

| Endpoint | One side (S) | ((q(S),h(S))) | Decision | Complement decision |
|---|---|---:|---|---|
| (H_e) | ({c_{e,i},x_d,y}) | ((0,1)) | length 3, (F_1) | length 4, (F_2) |
| (H_e) | ({u_e,x_d,y}) | ((-1,2)) | add one (x): length 4, (F_2) | (q=1), needs 232 unavailable (x)'s |
| (H_{ft}) | ({c_{e,i},c_f,u_t}) | ((0,1)) | length 3, (F_1) | length 4, (F_2) |
| (H_{ft}) | ({c_{e,i},u_f,u_t}) | ((-3,2)) | add three (x)'s: length 6, (F_2) | (q=3), needs 230 unavailable (x)'s |

Each full endpoint is a zero-core length-seven (F_3) block.  In total the
closure contains four (F_1) rows, seven (F_2) rows, two (F_3) rows, and
three rows with no available (X)-completion.  There is no endpoint-internal
middle-gap block and no endpoint-internal competing positive-core (F_3).
The prescribed block (X_4\sqcup U) itself has length seven and sum (3a).
This last check establishes its existence, not its global uniqueness.

## 4. All (P)-mixed target fibres

The two nonempty proper subsets of (P) are its singleton positions.  Their
((q,\rho))-labels are

\[
P_L:(2,-g),\qquad P_R:(1,g).
\]

For each singleton (A) and every (T\subseteq Q_H) with
(\rho(T)=-\rho(A)), the long-complement criterion requires

\[
q(A)+q(T)\in\{1,2,3\}.
\]

An exhaustive bounded-count enumeration gives:

| (Q_H) | target (g) for (P_L) | after adding (q(P_L)=2) | target (-g) for (P_R) | after adding (q(P_R)=1) |
|---|---|---|---|---|
| (Q_e) | ({0,1}) | ({2,3}) | ({0,1}) | ({1,2}) |
| (Q_{ft}) | ({-1,0,1}) | ({1,2,3}) | ({0,1,2}) | ({1,2,3}) |

Thus the universal quantifier over (T), for both singleton choices and both
displayed (Q_H), is genuinely checked.  This is not merely a check of one
witness (T).

## 5. Exact global-short boundary

The displayed lift cannot be promoted unchanged to the full automatic-short
spectrum.  Let (k_g^★) denote the exceptional (K:g) position labelled
((2,0,g)).  Then the literal block

\[
R=\{c_{e,1},k_g^★,c_f\}
\]

has length three and

\[
\sigma_{q,\rho}(R)=(0,e+g+f)=0,
\qquad
\sigma_h(R)=1+2-1=2.
\]

A quotient-zero block of length three can only be an (F_1) block and must
have actual height (1).  Therefore (R) is a concrete violation.  It lies
outside both displayed endpoints, so it does not contradict the exhaustive
endpoint-internal result.

The exact remaining existential question is:

> Does fixed Model C admit some other simultaneous height/(q) lift and some
> two-position (P) that preserve the two full mixed target fibres and the
> multiplicity cap while satisfying every global automatic short block?

Even a positive answer would still leave the complete four-edge incidence,
the global length (9,…,468) gap, all derived (F_3)-complement atoms, the
length-697 complement atom, Hasse rows, block-intersection constraints, and
actual (Z)-atomicity.

## Reproduction

Run `unique_tail_p233_doubleton_NC_lift_attack.py`.  It writes
`unique_tail_p233_doubleton_NC_lift_attack_report.json` and checks all claims
above without importing a production artifact.  The canonical report
certificate is

```text
194b0479c40009326d5330b1c234eaa969e4695165046145fac960c98a06b26f
```
