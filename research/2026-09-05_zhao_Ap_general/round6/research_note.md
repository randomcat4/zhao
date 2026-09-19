# Round 6: weighted top shadows, correction, and the over-deletion transform

Date: 2026-09-07

## Status

This round does **not** prove `A_p`, does **not** prove `h(S)<=p-5`, and does not produce a counterexample. The strongest unconditional height result remains

\[
\boxed{h(S)\le p-4}.
\]

A proposed shortcut from the continuation thread,

\[
\theta=-1\Longrightarrow \sigma(R)=0,
\]

is **retracted**. The error is isolated below. The augmented-coordinate setup, top-degree sign, the incidence identity `Lambda_i=W_i`, and the derivative identity are valid; the value of `Lambda_i` was misread.

Throughout, quantities with a tilde are integer counts. Untilded weights/parameters are in `F_p`; vector-sum identities are in `G=F_p^4`.

## 1. Exact audit of the retracted shortcut

Let `S=a^(p-4) R`, `|R|=4p`, and write `v_i=r_i-a`. Use the augmented group

\[
\widehat G=F_p\oplus G,
\qquad (m,g)\mapsto(m,g-ma).
\]

This is a linear automorphism; it is not an illegal affine translation in `G`.

In `F_p[G]`, with `y_nu=X^{e_nu}-1`, the augmentation ideal has top nonzero degree

\[
\Delta=4(p-1)=4p-4,
\]

and

\[
\Omega=\prod_{nu=1}^4 y_nu^{p-1}=\sum_{g\in G}X^g.
\]

Since `1-X^g=-ell_g+O(I^2)` and `Delta` is even, there is no missing global minus sign in a top-degree product.

For a four-position set `B subset R`, define the shifted top shadow by

\[
\prod_{j\notin B}(1-X^{v_j})=\widehat\omega_B\Omega,
\qquad
\widehat W_i=\sum_{B\ni i}\widehat\omega_B.
\]

Deleting `r_i` in the augmented product leaves `p-4` pure anchor factors, so obtaining `u^(p-1) Omega` requires exactly three additional `u` choices from `R\{i}`. Hence

\[
\boxed{\Lambda_i=\widehat W_i\quad\text{in }F_p.}
\]

The corresponding integer alternating count is

\[
\widetilde\Lambda_i
 =1-Z_p(S\setminus r_i)+Z_{2p}(S\setminus r_i)
  -Z_{3p}(S\setminus r_i)+Z_{4p}(S\setminus r_i).
\]

The counterexample hypothesis kills the `p` and `2p` layers. The `4p` layer is impossible as well: a `4p` zero-sum would contain a nonempty zero-sum of length at most `4p-3`; its complement inside the `4p` zero-sum would then have length at most `p+1<=3p-2`.

Thus

\[
\widetilde\Lambda_i=1-Z_{3p}(S\setminus r_i)\in Z.
\]

But the already proved one-position deletion congruence gives

\[
Z_{3p}(S\setminus r_i)\equiv1\pmod p.
\]

Therefore the correct conclusion is

\[
\boxed{\Lambda_i=\widehat W_i=0\quad\text{in }F_p,}
\]

not `1`. At the integer level one only knows

\[
\widetilde\Lambda_i\in pZ.
\]

Consequently the derivative identity

\[
\sum_i \widehat W_i v_i=0
\]

is valid but degenerates to `0=0`; it does not imply `sum_i v_i=0`.

The analogous shortcut in the conditional `3p`-atom four-block family is also invalid: degree uniformity there is on the atom `T`, so its vector double count only recovers `sigma(T)=0`, not `sigma(R)=0`.

## 2. General unshifted top shadow

Assume the archived `p-r` boundary normal form is valid, with `r>=4`, `p>=2r-1`,

\[
x_j\equiv 1_{j=0}+\sum_{s=0}^{r-4}\theta_s\binom r{j-s}\pmod p.
\]

Let `n=4p+r-4=Delta+r`. For `|B|=r`, define

\[
\prod_{i\notin B}(1-X^{g_i})=\omega_B\Omega,
\qquad
W=\sum_B\omega_B,
\qquad
W_i=\sum_{B\ni i}\omega_B.
\]

Then exact binomial summation gives

\[
\boxed{W=-\sum_{s=0}^{r-4}(-1)^s\theta_s.}
\]

For the marked degrees,

\[
d_j(i)=\sum_{s=0}^{r-3}\alpha_{i,s}\binom{r-1}{j-s},
\]

and

\[
\boxed{W_i=\sum_{s=0}^{r-3}(-1)^s\alpha_{i,s}.}
\]

Moreover the zero-sum vector identity on every length layer implies

\[
\sum_i\alpha_{i,s}g_i=0\quad\text{for every }s.
\]

Thus the point-weight vector equation is an alternating combination of already-zero marked vector moments and cannot by itself force the unweighted total sum `sigma(R)`.

More generally, the coefficient of the global positive-degree moment in the `q`-fold derivative identity is identically zero for every `1<=q<=r`. Hence ordinary point weights and positive-degree global vector moments are blind to the free `theta_s` parameters.

## 3. Over-deletion transform: all free parameters become visible

For `d>=r`, define

\[
Q_d=\sum_{|B|=d}\prod_{i\notin B}(1-X^{g_i}),
\qquad
F_d=[X^0]Q_d\in F_p.
\]

Its integer lift is

\[
\widetilde F_d
 =\binom nd+\sum_j(-1)^{j+1}\binom{n-3p-j}{d}x_j\in Z,
\qquad F_d=\widetilde F_d\bmod p.
\]

For `0<=q,s<=r-4`, substitution of the normal form gives

\[
\boxed{
F_{r+q}=\sum_{s=0}^{r-4}
 (-1)^{q+s+1}\binom{q+s+3}{q}\theta_s.
}
\]

The matrix

\[
M_{q,s}=(-1)^{q+s+1}\binom{q+s+3}{q}
\]

has

\[
\boxed{\det M=(-1)^{r-3}.}
\]

Therefore

\[
(F_r,\ldots,F_{2r-4})
\longleftrightarrow
(\theta_0,\ldots,\theta_{r-4})
\]

is an integer-unimodular transform. In particular, in a genuine `x_0=0` branch one has `theta_0=-1`, so at least one of these over-deletion residues is nonzero.

## 4. Geometric consequence of a nonzero residue

If `F_{r+q}!=0`, then some `B`, `|B|=r+q`, has

\[
U=R\setminus B,
\qquad |U|=4p-4-q,
\]

with

\[
\prod_{u\in U}(1-X^u)\ne0.
\]

For every linear subspace `V<=G`, necessarily

\[
|U\cap V|\le(p-1)\dim V.
\]

Hence, by the matroid partition criterion, `U` is the union of `p-1` linearly independent position sets, with total rank defect `q`. For `q=0`, `U` is a disjoint union of `p-1` four-element bases.

Define the signed subset-sum coefficient function

\[
c_U(x)=\sum_{Y\subseteq U,\ \sigma(Y)=x}(-1)^{|Y|}.
\]

It is a nonzero polynomial function on `G` of degree at most `q`, and complementing subsets gives

\[
\boxed{c_U(\sigma(U)-x)=(-1)^q c_U(x).}
\]

If `sigma(U)` lies on the anchor line `H=<a>`, then `c_U|_H` has at most `q` zeros. Combining this with reflection symmetry and the fact that only coefficients `0,1,...,r-1` cannot be cancelled by at most `p-r` anchors yields

\[
\boxed{p-q>2r\Longrightarrow \sigma(U)\notin H.}
\]

This is a strict structural reduction, not yet a contradiction.

## 5. The actual `h=p-4, x_0=0` conclusion

Here `r=4` and

\[
F_4=-\theta.
\]

The hard branch has `theta=-1`, hence

\[
\boxed{F_4=1.}
\]

Therefore there exists a four-position complement `B=R\setminus U` with

\[
|U|=4p-4,
\qquad
\prod_{u\in U}(1-X^u)\ne0.
\]

Consequences:

1. `U` is a disjoint union of `p-1` four-element bases;
2. `c_U(x)` has degree zero and is a nonzero constant, hence **every** group element is represented as a subset sum of `U` with nonzero signed coefficient;
3. for `p>=11`, `sigma(U) notin <a>`;
4. for `p=7`, if `sigma(U) in <a>`, reflection-orbit checking leaves only `sigma(U) in {0,-a}`.

This does **not** yet exclude the branch. The next required step is length control: refine

\[
\prod_{u\in U}(1-zX^u)
\]

by subset-size residue modulo `p`, or exploit the `p-1` basis decomposition, and combine a controlled representation with the four-point complement `B` and the `p-4` anchors to obtain an actual zero-sum of length at most `3p-2`.

## 6. Conditional `r=5` module

This section is conditional on first proving that all counterexamples have height at most `p-5`. It must not be used before the `p-4` boundary is closed.

For `r=5`, the normal form has two parameters and the first two over-deletion residues are

\[
F_5=-\theta_0+\theta_1,
\qquad
F_6=4\theta_0-5\theta_1,
\]

with determinant `1`. If `x_0=0`, then `theta_0=-1` and

\[
5F_5+F_6=1.
\]

Thus either a five-position deletion yields a top nonzero complement of length `4p-4`, or (in the unique `theta_1=-1` subcase) a six-position deletion yields a near-top nonzero complement of length `4p-5`. This is the first concrete instance of the general unimodular over-deletion mechanism.

## 7. Strict frontier

- Unconditional height theorem: `h(S)<=p-4`.
- Retracted: `theta=-1 => sigma(R)=0` and the derived claim `h(S)<=p-5`.
- New unconditional structure in the genuine `h=p-4, x_0=0` branch: a four-position complement `U` of length `4p-4` with nonzero top group-algebra product, a `p-1` basis partition, and constant nonzero signed subset-sum function.
- New general mechanism: the first `r-3` over-deletion residues recover all `theta_s` via an integer-unimodular matrix.
- Current target: convert the signed “every group element is represented” statement for `U` into a representation with usable length control, then combine with the four missing positions and anchors.
