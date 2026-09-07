# Fifth independent audit: excess deletions, basis partition, and B-side new reductions

Date: 2026-09-07

Source boundary: at audit time the named latest B-side manuscripts were not present on the three readable repository branches. The A-side statements below were independently reconstructed from the archived normal form. The B-side verdicts distinguish verified common interfaces from missing proof bridges.

## A. Excess deletion transform and unimodularity

For anchor height `h=p-r`, write

`x_j = 1_{j=0} + sum_{s=0}^{r-4} theta_s C(r,j-s) mod p`.

For formal excess deletion level `d=r+q`, `0<=q<=r-4`, define `F_{r+q}` by continuing the deletion polynomial beyond the legal Davenport deletion range. Then

`F_{r+q} = sum_s (-1)^{s+1} C(-4-s,q) theta_s`.

The matrix

`M_{q,s}=(-1)^{s+1} C(-4-s,q)`

has determinant `(-1)^(r-3)`. After row/column signs it is the evaluation matrix of the integer-valued polynomials `C(s+q+3,q)` at consecutive integers; its determinant is 1. Hence the correspondence

`(F_r,...,F_{2r-4}) <-> (theta_0,...,theta_{r-4})`

is unimodular over the integers and therefore bijective modulo every prime.

Hidden quantifiers: the `F_d` for `d>=r` are formal excess-deletion residues, not valid deletion congruences forced to vanish. The prior length compression still carries its own parameter range assumptions.

## B. A-side x_0=0: existence of U and partition into p-1 bases

For `r=4`, `x_0=0` gives `theta=-1`, hence the first excess residue satisfies `F_4=1` in `F_p`.

Summing the top socle coefficients over all four-position deletions therefore produces a nonzero total, so at least one deletion `B_0` has

`U=R\B_0`, `|U|=4p-4`,

and

`prod_{u in U}(1-X^u)=omega J_G != 0`.

If a position subset `A subset U` spans a `t`-dimensional subspace and `|A|>t(p-1)`, its subgroup-algebra augmentation product vanishes. This would force the whole product for `U` to vanish, contradiction. Hence

`|A| <= (p-1) rank(A)` for every position subset `A`.

By the matroid partition theorem, `U` is a disjoint union of `p-1` independent sets. Since `|U|=4(p-1)` and the ambient rank is 4, every part has size 4 and is a basis.

## C. Length-layered representability for the deleted four positions

Let `D=R\U` be the four deleted positions. For every nonempty `C subset D`, any `A subset U` with `sigma(A)=-sigma(C)` makes `A union C` a zero-sum subset of `R`.

In the `x_0=0` branch the only nonempty zero-sum lengths in `R` are `3p+1,...,3p+4`. Therefore

`N_k^U(-sigma(C))=0`

unless

`k in {3p+1-|C|,...,3p+4-|C|}`.

The signed fibre sum over those four permitted lengths is `omega != 0 mod p`; hence at least one of the four layer counts is nonzero modulo `p`.

This is a genuine length-layered strengthening for the 15 nonempty subsums of the deleted four-position set. It does not imply a uniform short representation theorem for every group element.

## D. B-side: maximum-support complement near-squarefree

The archived interface gives, for every `(p-3)`-position set `E`, a completion degree divisible by `p`. If `R` has at least two support defects, two redundant positions can be deleted while preserving `supp(R)`, yielding such an `E`.

Maximality of `supp(R)` forces every completion of this `E` to use old support values. What is not supplied by the archived interface is the needed assertion that old-support completions cannot themselves total a positive multiple of `p`.

Verdict: **needs a cross-link / clean-completion lemma**. A single completion link plus the local multiplicity and linear-functional constraints does not force support growth.

## E. B-side: rank-three unique-double exclusion

The reliable comparison identity is

`mu_R(g) = ell_R(g)+lambda_T(g) = 2(nu_S(g)-nu_R(g)+1)`.

If a neighbouring maximum-support complement moves the unique doubled value from `a` to `x`, while the multiplicity-stable common values span the same rank-three space, then `mu_R` and `mu_R'` agree on a spanning set but differ by `-2` at `x`, contradiction.

Hidden requirements: existence of such a clean maximum-support neighbour and the spanning condition. If the moved value is a coloop of the common set, the common stable values need not determine the whole rank-three functional.

Verdict: **conditional comparison core valid; full exclusion needs clean completion plus a non-coloop/spanning argument.**

## F. B-side: squarefree rank-three with coloop / two-element cocircuit

The matroid reductions are valid: deleting a coloop (and one suitable additional element), or deleting a two-element cocircuit, produces a `(p-3)`-position common set of rank two to which the high-order completion congruence applies.

The missing bridge is again value-changing maximum-support completion. The degree divisible by `p` may be absorbed by positional copies or lower-support completions. To close the branch one needs a decomposition

`d(E)=d_copy(E)+d_lower(E)+d_change(E)`

and a proof that `d_change(E)>0` for at least one selected coloop/cocircuit link. A congruence excluding `d_copy+d_lower == 0 mod p` would suffice.

Verdict: **matroid setup valid; exclusion still needs a clean-completion lemma and, in rank-two common intersections, usually a second-neighbour comparison.**
