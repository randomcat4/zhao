# Round 6 audit / boundary ledger

Status: mathematical self-audit and exact finite-arithmetic verification; not a proof-assistant certificate and not an exhaustive enumeration of `F_p^4` sequences.

## Retraction

The continuation claim

\[
\theta=-1\Rightarrow\sigma(R)=0
\]

is invalid and must not be used. The exact error is

\[
\Lambda_i=1-Z_{3p}(S\setminus r_i)\equiv0\pmod p,
\]

because `Z_{3p}(S\setminus r_i)≡1`, whereas it was previously read as `Lambda_i=1`.

The following pieces survive the audit:

- augmented linear-coordinate change;
- top-degree sign convention;
- `Lambda_i=W_i` incidence identity in `F_p`;
- derivative/vector identity;
- all distinctions between integer lifts and reductions modulo `p` in `research_note.md`.

## Strict current theorem

Every hypothetical counterexample still satisfies only

\[
\boxed{h(S)\le p-4}.
\]

No `h<=p-5` claim is certified.

## New verified interfaces

1. General `p-r` scalar normal form was rechecked as an integer-valued binomial identity.
2. Unshifted top `r`-shadow total weight equals `-sum_s (-1)^s theta_s`.
3. Marked point weights equal the alternating sum of the marked finite-difference parameters.
4. Every positive-degree global moment coefficient cancels identically.
5. The over-deletion residues `F_r,...,F_{2r-4}` are an integer-unimodular transform of `theta_0,...,theta_{r-4}`.
6. For `r=4`, `x_0=0` implies `F_4=1`; hence some four-position complement has nonzero top group-algebra product.
7. A direct lower-dimensional group-algebra calculation independently checks the top-sign/incidence convention.
8. Small-prime anchor-line orbit degeneracies were separately checked for `(r,p)=(4,7)` and `(5,11)`.

## What is not certified

- `A_p`;
- `h<=p-5`;
- impossibility of the `h=p-4, x_0=0` branch;
- any statement that point-degree uniformity forces an unweighted total sum;
- the conditional `r=5` module before `h=p-4` is closed.

## Next target

For the `r=4, x_0=0` complement `U`, study

\[
\prod_{u\in U}(1-zX^u)
\]

and split the constant signed subset-sum coefficient by subset length modulo `p`. The goal is to produce a representation that, after using the four missing positions and at most `p-4` anchors, yields an actual zero-sum of length at most `3p-2`.
