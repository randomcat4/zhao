# Squarefree nineteen-position theorem and the B endpoint

STATUS: **PROVED candidate, awaiting fresh independent verification.** The conclusion below excludes the entire squarefree class of B, but does not prove B for sequences with repeated values. A remains unresolved by this note.

Work directory was confirmed as `C:/game/gameproject/showa100`. No access to `C:/canglan`, no child agents, and no external computation service were used. This is the independent `global_endpoint_proof` route. No novelty or Lean-verification claim is made.

## 1. Statement, conventions, and dependencies

**Theorem.** Every set of nineteen distinct elements of `G = F5^4` contains a nonempty zero-sum subset of size at most fourteen.

Every subset below is a subset of positions. Distinctness means that distinct positions carry distinct actual group elements. We make no affine translation of the sequence. Only this auxiliary theorem imposes distinctness; the original A/B targets continue to allow repetitions.

We use the following known inputs.

1. `D(C5^4) = 17`. Thus every nonempty minimal zero-sum sequence has length at most seventeen.
2. For every sequence U of at least seventeen positions,

       sum_j (-1)^j Z_j(U) = 0  (mod 5).

   This is the usual group-ring zero-sum congruence. A short derivation is included below.
3. `SD(C5^4) = 16`, in the convention that SD is the maximum length of a squarefree minimal zero-sum sequence. This definition is explicitly given in Definition 3.1 and the paragraph following it (printed pp. 720–721) of Ordaz–Philipp–Santos–Schmid, *On the Olson and the Strong Davenport constants*, JTNB 23 (2011). The value is stated in Theorem 8.1(3), printed p. 744, and the computation is discussed on printed p. 747. The published PDF was opened and these conditions were checked: <https://jtnb.centre-mersenne.org/item/10.5802/jtnb.784.pdf>. No statement about all sequences of length sixteen is inferred from SD.

For input 2, work in `F5[G]`, write `y_i = X^{e_i}-1`, and use `y_i^5=0`. The augmentation ideal has seventeenth power zero, since any surviving monomial has each of its four exponents at most four. Consequently `prod_{g in U}(1-X^g)=0` for `|U|>=17`. Its identity coefficient is the displayed alternating count, including `Z_0=1`.

Assume towards contradiction that S consists of nineteen distinct elements and has no nonempty zero sum of length at most fourteen. In particular its elements are nonzero and it has no opposite pair. Since two nonempty zero sums would have total length at least thirty if disjoint, every zero-sum subset of S is minimal: a proper zero-sum subset would leave a disjoint nonempty zero-sum complement. Inputs 1 and 3 imply that all its nonempty zero sums have lengths fifteen or sixteen.

## 2. A sixteen-atom admits at most one new distinct safe element

**Lemma 2.1.** Let T be a squarefree minimal zero-sum sequence of length sixteen in `F5^4`. Suppose `T g h` is squarefree, where g and h are two further elements. Then `T g h` contains a nonempty zero sum of length at most fourteen.

**Proof.** Suppose no such short zero sum exists. For a group element z, let `P_T(z)` count the unordered pairs of distinct positions of T whose values sum to z.

Fix `z` equal to g or h and consider the seventeen-position sequence `T z`.

- A fifteen-position zero sum must include z, since a proper nonempty subset of the atom T is not zero-sum. It is obtained by deleting a pair from T of sum z. Hence `Z15(T z)=P_T(z)`.
- The only sixteen-position zero sum is T itself. A different one would replace a single T-value a by z and require `a=z`, contrary to squarefreeness. Hence `Z16(T z)=1`.
- The total sum of `T z` is the nonzero value z, so `Z17(T z)=0`.

The alternating congruence gives

    1 - P_T(z) + 1 = 0 (mod 5),
    P_T(z) = 2 (mod 5).

For fixed z, its pair representations in a squarefree T form a matching: two different pairs sharing one position would force their other values to agree. This matching has at most four edges. Indeed, any five disjoint pairs would have total sum `5z=0`, giving a ten-position zero sum inside T. Therefore `P_T(z)=2` exactly.

Write the two disjoint g-pairs as `{a,b}` and `{c,d}`; these are four distinct actual values and

    a+b = c+d = g.

Every h-pair must intersect each of these two g-pairs. Otherwise deleting a disjoint g-pair and h-pair from the zero-sum T and inserting g and h would give a zero sum of length `16-4+2=14`.

An h-pair therefore has one endpoint in `{a,b}` and one in `{c,d}`. Since the two h-pairs are disjoint, they form one of the two crossing perfect matchings on these four values. After interchanging c and d if necessary, write them as `{a,c}` and `{b,d}`. Thus

    a+c = b+d = h.

Subtracting the two displayed equality relations gives `2(b-c)=0`. Multiplication by two is invertible in `F5^4`, so `b=c`, contradicting the four distinct values. This proves the lemma.

Consequently S cannot contain a sixteen-position zero sum: such an atom has three outside positions in S, and any two contradict Lemma 2.1. All nonempty zero sums in S therefore have length fifteen.

## 3. Fifteen-atoms cannot differ in one or two positions

Let A and B be different fifteen-position zero sums in S. They cannot differ in a single position, since exchanging one value in a zero sum for another requires equality of those two values.

Suppose they differ in exactly two positions. Let x and y be the two positions of `B\A`, and put `z=x+y`. The seventeen-position sequence `U=A x y` has only fifteen-position nonempty zero sums, as it is a subsequence of S.

There is one fifteen-zero-sum using neither x nor y, namely A. A fifteen-zero-sum using exactly one of x or y would replace a single A-value by that same value, impossible by squarefreeness. Those using both x and y are precisely the complements of pairs of A summing to z. If `P_A(z)` counts these pairs, then

    Z15(U) = 1 + P_A(z).

The alternating congruence gives `P_A(z)=0 (mod 5)`. As in Lemma 2.1, these pairs form a matching and five disjoint pairs would yield a ten-position zero sum. Thus `0<=P_A(z)<=4`, and `P_A(z)=0`. But the two positions of `A\B` form one such pair, a contradiction.

It follows that any two distinct fifteen-zero-sums differ in at least three positions.

## 4. Packing and the deletion count contradict one another

For each fifteen-zero-sum A in the nineteen-position S, take its four-position complement `C=S\A`. Section 3 says that any two distinct such complements intersect in at most one position. Therefore no unordered pair of positions can occur in two complements. Each complement contains six pairs, whereas S has `binom(19,2)=171` pairs. Hence

    6 Z15(S) <= 171,
    Z15(S) <= 28.                                      (1)

On the other hand, each seventeen-position subsequence U of S has a zero sum by D=17. All those zero sums have length fifteen, so `Z15(U)>=1`.

Fix an eighteen-position subsequence W. Summing the preceding inequality over its eighteen one-position deletions counts each fifteen-zero-sum exactly three times. Thus

    3 Z15(W) >= 18,
    Z15(W) >= 6.

Now sum over the nineteen eighteen-position subsequences W of S. Each fifteen-zero-sum is counted four times, giving

    4 Z15(S) >= 19*6 = 114,
    Z15(S) >= 29.                                      (2)

Inequalities (1) and (2) contradict each other. This proves the theorem. The stronger already-known residue `Z15(S)=1 (mod 5)` would improve (2) to 31, but is not needed for this proof.

## 5. Exact scope and remaining gap

Every squarefree twenty-position sequence contains a squarefree nineteen-position subsequence, so the theorem excludes the complete multiplicity class `a=b=0` at B. The original B statement remains open here because it permits repeated group elements.

The matching argument is the exact place where distinctness matters. With repeated values, the pairs of a fixed sum form complete bipartite pieces (and possibly a clique on equal half-values), rather than a matching. Consequently five pair representations need not occupy ten distinct positions, and `P_T(z)=2 (mod 5)` need not force `P_T(z)=2`. Likewise, a one-position exchange between atoms can be legal when the values agree. No unproved extension of either step to repeated sequences is used.

The earlier eighteen-position construction with multiplicity four does not contradict this theorem. Neither does a squarefree eighteen-position configuration, if one exists: this proof requires nineteen positions for the final packing contradiction.

Endpoint verdict of this route: **B proved for squarefree sequences only; full B INCOMPLETE; A INCOMPLETE.**
