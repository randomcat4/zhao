# An eighteen-element squarefree core cannot be extended

STATUS: **PROVED candidate, awaiting fresh independent verification.** This note depends on the separately frozen squarefree nineteen-position candidate `global_continue_squarefree_B.md`; it does not alter that candidate. No complete B or A proof is claimed.

Work directory: `C:/game/gameproject/showa100`. No `C:/canglan` access, child agent, or external compute was used.

## 1. Auxiliary theorem

**Theorem.** If T consists of eighteen distinct elements of `F5^4` and has no nonempty zero-sum subset of length at most fourteen, then adjoining any one group element creates such a short zero sum.

If the new value is not in T, the preceding squarefree nineteen-position theorem applies. It remains to prove that adding another copy of an existing value v also creates a short zero sum. The proof below is only for this repeated-value case.

Assume to the contrary that `S=T v` has no nonempty zero sum of length at most fourteen. In particular `v!=0` and `0` is not a value of T. Every nonempty zero sum in S is an atom and has length at most seventeen, because a nonminimal zero sum would contain two disjoint zero sums of total length at least thirty.

## 2. The six triples in T

The proof of Lemma 2.1 in `global_continue_squarefree_B.md` shows that T has no sixteen-atom: such an atom would have two distinct outside values in T. The published `SD(C5^4)=16` excludes a squarefree seventeen-atom. Therefore the only nonempty zero sums in T have length fifteen.

Section 3 of the same note applies to any two fifteen-zero-sums in T and shows that they cannot differ in one or two positions. Their three-position complements in T are consequently disjoint. There are thus at most six of them.

Each of the eighteen seventeen-position deletions of T contains a zero sum, by `D(C5^4)=17`. It has length fifteen. Each fifteen-zero-sum is counted in three deletions, so there are at least six. Hence there are exactly six, and their complements partition T into six triples `C_1,...,C_6`. Each `T\C_i` is a fifteen-atom. These triples are sets of positions with distinct actual values.

Let C be the triple containing the old position with value v.

## 3. A forced translation for the fifteen values outside C

Fix a position x of `T\C`, and let `C_j` be its triple. Put `A=T\C_j`. Then A is a squarefree fifteen-atom containing the old copy of v but not x. The sequence

    U = A (new v) x

has seventeen positions and is an actual subsequence of S. The new v position is distinct from the old v position in A. Write `z=v+x`, let `P_A(z)` count unordered pairs of A summing to z, and let `m_A(z)` be the multiplicity of z in A, which is either zero or one.

The zero-sum counts in U are exactly

    Z15(U) = 2 + P_A(z),
    Z16(U) = m_A(z),
    Z17(U) = 0.

For the first formula, one fifteen-zero-sum is A, a second replaces its old v by the new v, and those using both extra positions are obtained by deleting a pair of A of sum z. A zero sum using x but not the new v would require x to equal an A-value, which it does not. A sixteen-zero-sum must delete an A-value equal to z; deleting either extra position leaves total sum v or x, both nonzero. Finally, the total sum of U is z, which is nonzero because v and x together would otherwise be a forbidden two-position zero sum.

The seventeen-position alternating congruence therefore gives

    P_A(z) - m_A(z) = 4 (mod 5).                       (1)

For a fixed z, the pair representations in the squarefree A form a matching. There cannot be four such pairs: their eight positions together with the new v and x would be ten distinct positions summing to `4z+v+x=5z=0`. Thus

    0 <= P_A(z) <= 3,   0 <= m_A(z) <= 1.

The integer on the left of (1) lies in `[-1,3]`. Its only value congruent to four modulo five is minus one. Consequently

    P_A(z)=0,  m_A(z)=1,
    x+v = z is a value of A, hence a value of T.        (2)

This holds for every one of the fifteen positions x outside C.

## 4. The translation paths cannot hold eighteen distinct values

Consider translation by the nonzero vector v on G. Its orbits have length five. No full orbit is contained in T: the sum of an orbit

    a, a+v, a+2v, a+3v, a+4v

is `5a+10v=0`, a forbidden five-position zero sum.

On each translation orbit, the subset of values belonging to T is therefore a disjoint union of directed paths, each with at most four vertices. Every such path has a last vertex y for which `y+v` is not in T. Equation (2) says every last vertex must belong to the three-element set C.

The path containing v starts at v, because its predecessor under translation is zero and zero is not in T. It has at most four vertices. If its last vertex is v, this path contains just one vertex. If it has any later vertices, its last vertex is one of the other two elements of C.

In all cases there are at most three paths, each of length at most four, and hence

    |T| <= 3*4 = 12,

already contradicting `|T|=18`.

The sharper count `1+4+4=9` is not needed and is not asserted here: (2) is not imposed on v itself, so the path containing v is not known to end at v. The correct uniform bound twelve suffices.

This proves the repeated-value case and hence the theorem.

## 5. Consequence for the original B endpoint

Suppose a twenty-position B counterexample had at least eighteen distinct values. Select eighteen positions with distinct values. There is at least one remaining position, whether its value is new or repeated. The auxiliary theorem gives a short zero sum in those nineteen positions, contradicting badness.

Therefore every B counterexample must satisfy

    |supp(S)| <= 17,
    2a+b = 20-|supp(S)| >= 3.

Combined with the independently established upper bound `2a+b<=7`, a B counterexample would have `3<=2a+b<=7`. This excludes complete B classes of cumulated multiplicity zero, one, and two, including `(a,b)=(0,0),(0,1),(0,2),(1,0)`. No claim about the remaining classes or A follows from this note.
