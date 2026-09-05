# Atom and subgroup structure route

STATUS: **INCOMPLETE** for both frozen endpoints A and B. The lemmas below are complete necessary conditions, not a proof of either endpoint. The scope is p=5 unless explicitly stated otherwise. No hypotheses in the frozen statement were changed.

Working directory: `C:/game/gameproject/showa100`. No access to `C:/canglan`, child agents, Euler, or paid computation was used by this route.

## 1. Explicit external dependencies

The full local text of Zhao--Hong, *On zero-sum subsequences over finite abelian groups of length not exceeding a given number*, was read at `math/2026-09-04_zhao_response/proofs/zhao_hong_2026.txt`.

The following statements are **KNOWN**, specifically as stated in its Lemma 2.3:

* (ii): s_{<=9}(C_5^3)=17 and s_{<=10}(C_5^3)=15. It also states s_{<=8}(C_5^3)=18.
* (iv): s_{<=k}(C_5^2)=18-k for 5<=k<=9. Thus the values needed here are s_{<=5}=13 and s_{<=6}=12.
* (v): s_{<=D(G)-2}(G)=D(G)+1 for G=C_p^r with 3<=r<p. Taking p=5,r=4 satisfies every stated condition and gives s_{<=15}(C_5^4)=18.

These are being used as explicit published dependencies, not claimed as new results of this route. The item (ii) points to Aleen Sheikh's 2017 thesis. The [university thesis record](https://pure.royalholloway.ac.uk/en/publications/the-davenport-constant-of-finite-abelian-groups/) was read; its linked PDF returned HTTP 403, so this route did not independently audit the thesis computation. The actual mathematical statement used was read in the published Zhao--Hong lemma. The statement in (v) is likewise read directly in that lemma, with its condition r<p checked.

The frozen facts D(C_5^d)=4d+1 and the position-count congruences are also used. The proof below never extends the displayed p=5 constants to arbitrary p.

## 2. PROVED_HERE: subgroup occupancy restrictions

Let S be a hypothetical bad sequence for A (|S|=21, no nonempty zero sum of length <=13) or B (|S|=20, none of length <=14).

### Lemma 2.1: maximal zero-sum-free sequences cover their subgroup

If V is zero-sum-free in a finite abelian group H and |V|=D(H)-1, every h in H is the sum of a subsequence of V, allowing the empty subsequence.

For h=0 use the empty subsequence. If h!=0 were missing, V followed by -h would be zero-sum-free: any new zero sum must use -h and hence a subsequence of V summing to h. This would be a zero-sum-free sequence of length D(H), a contradiction.

### Lemma 2.2: every one-dimensional subgroup contains at most three positions of S

Suppose a line H contains four positions, forming V. Those four terms are zero-sum-free, since a zero sum of length <=4 is forbidden. Since D(H)=5, Lemma 2.1 gives all of H as subsequence sums of V, with representatives of length at most four.

Project S/V to G/H=C_5^3. In A it has 17 terms, so the published s_{<=9}=17 gives a nonempty projected zero sum Q of length <=9. Its actual sum belongs to H and can be cancelled by at most four terms of V. The resulting nonempty zero sum has length <=13. In B, S/V has 16 terms, so s_{<=10}=15 gives Q of length <=10, leading to a zero sum of length <=14. Both contradict badness.

If a line initially contained more than four positions, select any four; the same argument applies. In particular, **h(S)<=3**.

### Lemma 2.3: a line containing three positions contains three equal elements

The three terms on the line are zero-sum-free. Their elementary classification in C_5 is as follows. If three distinct nonzero residues occurred, a pair would be opposite, since C_5\{0} consists of two opposite pairs. If there are exactly two distinct residues, write the repeated term as g and the other as ag. For a=3 the sum 2g+ag is zero, and for a=4 an opposite pair occurs. Hence only a=2 is possible. The only nonconstant zero-sum-free triple is therefore g,g,2g, up to the choice of generator.

Its subsequence sums contain 0,g,2g,3g,4g, so it covers its line with representatives of length at most three. Projecting the other 18 terms in A or 17 terms in B to C_5^3 gives a nonempty zero sum of length <=9, by s_{<=9}=17. Cancelling its lift with at most three line terms gives a zero sum of length <=12, forbidden in both cases.

Thus a three-position line is monochromatic. In particular, if an element has multiplicity two or three, no different support element lies on its line.

### Lemma 2.4: every two-dimensional subgroup contains at most seven positions of S

Suppose H=C_5^2 contains eight positions V. The sequence V is zero-sum-free, and |V|=D(H)-1=8. Lemma 2.1 supplies a subsequence of V summing to each element of H, of length at most eight.

For A, the remaining 13 terms project to C_5^2 and s_{<=5}=13 supplies a nonempty projected zero sum of length <=5. Its lift can be cancelled using V, giving length <=5+8=13. For B, the remaining 12 terms and s_{<=6}=12 give length <=6+8=14. Both are forbidden.

All selections here are by positions; repeated elements cause no ambiguity, and the two pieces of each lifted zero sum are disjoint.

## 3. Independent audit of the six-triple computation

At the root agent's explicit request, this route read and audited `scripts/search_support7_cap3.ps1` and its completed log `evidence/search_support7_cap3.log`. This was an authorized cross-check of a produced computational object, not reading another route's uncompleted proof draft.

The logged result is:

    pairs=191890 surviveA=0 surviveB=0 candidatesA=0 candidatesB=0 badA=0 badB=0

Its stronger conclusion is that every sequence consisting of **six distinct elements each repeated three times** in C_5^4 has a zero sum of length <=13.

For a rank-four support, choose four of its six vectors as a basis and normalize to [I_4|a|b]. The remaining vectors a,b are distinct, nonzero, and different from the four basis vectors. There are 620 eligible choices and binomial(620,2)=191890 unordered pairs. Enumerating all such a<b loses nothing because both extra multiplicities are three.

For each pair the script checks t,u in {0,1,2,3}, except (0,0), and computes the basis coefficients as the four residues of -ta-ub. It accepts exactly when all four residues lie in {0,1,2,3}. The sum of those residues plus t+u is the actual subsequence length. Every nonempty zero sum under the six capacities is represented: a zero sum with t=u=0 would force all four basis coefficients to be zero. The script records the minimum of these lengths, and no pair had a minimum greater than 13. Its base-five group addition, negation as fourfold addition, residue-capacity test, and lengths were checked directly in the source.

If the six support vectors have rank at most three, their 18 terms already have a zero sum of length at most D(C_5^3)=13, so this missing-rank case is covered analytically. This is an exact finite computational dependency, not a proof for arbitrary primes, and not a Lean-checked theorem.

Together with Lemma 2.2 this excludes support size at most seven in both endpoints. More strongly, a bad S contains at most five elements of multiplicity three. For A with support seven all seven multiplicities would be three; for B with support seven six multiplicities are three and one is two. Each would contain six triples.

A separate general support-seven script was drafted here before the other route's completed stronger computation was communicated. It is retained as `scripts/atom_support7.ps1` but **was not run and is not used as evidence**.

## 4. PROVED_HERE: atom complements form covering families

Write z_j for the number of position-subsequences of S that are zero sums of length j. The frozen congruences give z_15=1 mod 5 and z_j=0 mod 5 for all other allowed j. Each position belongs to 0 mod 5 zero sums of each allowed length. Therefore, in the family of complements of j-atoms, each position has degree z_j mod 5.

The new ingredient in this section is s_{<=15}(C_5^4)=18, from Lemma 2.3(v) with r=4<p=5.

### Lemma 4.1: in B, z_15>=26

Delete any two positions from S. The remaining 18 terms contain a zero sum of length <=15. Badness for B excludes all lengths <=14, so there is a 15-atom disjoint from those two positions. Thus the five-position complements of all 15-atoms cover every pair of positions.

Let d_x be the number of these complements containing position x. Each such complement covers at most four of the 19 pairs containing x, hence 4d_x>=19. Also d_x=1 mod 5. Therefore d_x>=6. Summing over all 20 positions gives

    5 z_15 = sum_x d_x >= 20*6 = 120.

Since z_15=1 mod 5, this strengthens z_15>=24 to **z_15>=26**.

### Lemma 4.2: in A, 7 z_14 + 4 z_15 >=294

Delete any three positions from S. The 18 terms left contain a zero sum of length <=15, hence an atom of length 14 or 15. Thus the seven-position complements of 14-atoms and the six-position complements of 15-atoms jointly cover every triple of positions.

For a fixed position x, let d_14(x),d_15(x) be its degrees in these two complement families. A seven-position block containing x covers at most binomial(6,2)=15 triples containing x, and a six-position block covers at most binomial(5,2)=10. Hence

    15 d_14(x) + 10 d_15(x) >= binomial(20,2) = 190.

Write d_14(x)=5a_x and d_15(x)=1+5b_x. Here a_x,b_x are nonnegative integers; the degree congruences justify both forms, including d_15(x)>=1. Substitution and integer rounding give 3a_x+2b_x>=8. Summing over 21 positions and using the block sizes gives

    (21 z_14 + 12 z_15 -42)/5 >=168,

equivalently **7 z_14+4 z_15>=294**. If z_14=0, the congruence z_15=1 mod 5 gives z_15>=76.

## 5. PROVED_HERE: the six-atom equality structure and its consequence

Suppose z_15=6 in either endpoint, temporarily. Each position has complement degree in {1,6}, because its degree is 1 mod 5 and there are exactly six complements. Positions of degree six form a common core C; every other position belongs to exactly one complement. The core size c follows by counting incidences:

    6(N-15)=N+5c, so c=N-18.

Thus c=2 in B and c=3 in A. The six complements are C union P_i, where the P_i are pairwise disjoint three-position petals. Every 15-atom is the union of the other five petals. Subtracting their zero-sum equations shows all six petal sums are equal. These statements count positions and do not assert that the vectors in different petals are distinct.

B cannot have this structure, already by Lemma 4.1. In A, a stronger conditional count than Lemma 4.2 follows. At a core position d_15=6, the triple-covering inequality forces d_14>=10. At each of the other 18 positions d_15=1, it forces d_14>=15. Hence

    7 z_14 >=3*10+18*15=300.

As z_14 is a multiple of five, **z_15=6 in A implies z_14>=45**. In particular, six 15-atoms without any 14-atoms cannot realize A.

## 6. EXACT COMPUTATIONAL EXCLUSION: five distinct tripled elements

This section covers arbitrary support size, not only support eight. Its result is that a bad endpoint sequence has **at most four distinct elements of multiplicity three**.

### Five normalized cores are exhaustive

Suppose five distinct tripled elements occur. If their span has rank at most three, their 15 terms already contain a zero sum of length at most 13. Otherwise choose four independent ones and normalize their three copies each to

    V=e_1^3 e_2^3 e_3^3 e_4^3.

Write x for the fifth tripled element. For t=1,2,3, the possible relation using t copies of x and the four basis vectors has basis coefficients [-t x_i]_5. Any coefficient four is unavailable; otherwise its length is t+sum_i[-t x_i]_5.

The absence of zero sums of length <=13 forces the coordinates of x to contain each of 1,2,3:

* If no coordinate is 1, t=1 has all four coefficients at most three, giving length at most 13.
* If no coordinate is 3, t=2 has all coefficients at most three. Unless all four coefficients equal three, its length is at most 13. The exceptional case is x=(1,1,1,1), for which t=3 instead gives length 3+4*2=11.
* We now know x has a coordinate 1 and a coordinate 3. If it has no coordinate 2, the t=3 relation is available. Its basis coefficients at those two specified coordinates are 2 and 1, and the other two are at most three, giving length at most 3+2+1+3+3=12.

Conversely, if x contains 1,2,3, every t=1,2,3 requires a basis coefficient four (at a coordinate 1,3,2, respectively). Thus V x^3 is zero-sum-free. Coordinate permutations reduce x to exactly the following five possibilities:

    (0,1,2,3), (1,1,2,3), (1,2,2,3), (1,2,3,3), (1,2,3,4).

All core elements have the same multiplicity three, and the remaining elements are unrestricted, so coordinate permutations lose no case.

### Exact extension algorithm and scope

The executable is `scripts/atom_five_triples.py`; its complete output is `evidence/atom_five_triples.json`, including all initially admissible vectors, level counts, a longest extension, completion status, and the script SHA-256.

For a current sequence W, maintain d(h), the minimum length of a subsequence summing to h, with d(0)=0 for the empty subsequence and infinity for an unattained sum. Adjoining g is safe for endpoint cutoff m if and only if d(-g)+1>m. Every newly formed zero sum uses g, so this criterion is exact. The updated table is

    d_new(h)=min(d(h),1+d(h-g)).

All 625 group elements are encoded in base five and all arithmetic is exact. Zero is rejected automatically. Capacities are at most three by Lemma 2.2; no support-size restriction, positivity convention on coordinates, or additional classification assumption is imposed on new elements. The search visits extensions in nondecreasing encoded order, retaining repeated vectors until their capacity is full. Every multiset extension has such a unique order. The safe candidate list only shrinks because adding positions can only decrease d(h), so dropping an unsafe vector cannot delete a valid later extension.

Each of the five cores was independently extended with (N,m)=(21,13) and (20,14). All ten runs completed before the one-million-node safety limit; there were no terminal endpoint extensions. More strongly, every branch stopped at length at most 17.

| Core x | A: safe one-term extensions | A: safe two-term extensions | B: safe one-term extensions | B: safe two-term extensions |
|---|---:|---:|---:|---:|
| (0,1,2,3) | 127 | 312 | 126 | 63 |
| (1,1,2,3) | 29 | 35 | 25 | 12 |
| (1,2,2,3) | 29 | 35 | 25 | 12 |
| (1,2,3,3) | 29 | 35 | 25 | 12 |
| (1,2,3,4) | 29 | 35 | 25 | 12 |

In every row and both endpoints, the number of safe three-term extensions is zero. Consequently no bad endpoint can contain five distinct tripled elements. This is an exact finite computational conclusion for p=5. It has not been independently rerun or checked in Lean at the time this section was written.

The multiplicity consequence sharpens the remaining support possibilities: A needs support at least nine. B needs support at least eight, and support eight would force exactly four multiplicities three and four multiplicities two.

## 7. EXACT COMPUTATIONAL EXCLUSION: four independent tripled elements

This section eliminates either bad endpoint when four of its tripled elements are linearly independent. It does not address four tripled elements of rank three; that separate case was assigned to the root agent.

Normalize the four tripled elements to e_1,e_2,e_3,e_4. By Section 6 a bad sequence cannot contain any fifth tripled element, so every new support vector has capacity at most two. The core is the 12-position zero-sum-free sequence

    e_1^3 e_2^3 e_3^3 e_4^3.

The program `scripts/atom_four_independent.py` reuses the exact subsequence-distance functions from the five-core executable. It was run with the weaker common cutoff m=13, target length 21, a 45-second bound for the whole search, and a 100000-node bound for each root. Its completed output is `evidence/atom_four_independent_A.json`.

There are exactly 365 admissible first additions. The raw distance/capacity criterion is used in the program; equivalently, such a vector has a coordinate equal to one and is not one of the four saturated basis vectors. Indeed, if no coordinate is one, its negative has all four coordinates at most three and is represented in the core using at most twelve terms, giving a forbidden zero sum after the addition. If a coordinate equals one, its negative has a coordinate four, so it is not represented in the core.

### Why the 34 symmetry roots cover every extension

For a vector g, let o(g) be the numerically least base-five encoding of a coordinate permutation of g. Choose an added vector g minimizing o(g) over the entire added multiset, then apply a coordinate permutation pi with pi(g)=o(g). Every other added vector h satisfies

    pi(h) >= o(h) >= o(g)=pi(g).

Thus, after a permissible automorphism fixing the core as a multiset, the numerically first addition is itself the least member of its coordinate-permutation orbit. The program retains exactly these 34 first-addition vectors, recognizable by their coordinates being nonincreasing in low-to-high base-five order. It then visits all further additions in nondecreasing numerical order, using the same exact safety test and monotone candidate pruning as Section 6. No analogous symmetry restriction is imposed on later additions.

The resulting finite output is:

    initial_safe_candidates=365
    canonical_roots=34
    all_selected_roots_completed=true
    nodes=656175
    maximum_reached_length=18
    terminal_extensions=0

Every root completed exhaustively: the largest root had 88013 nodes, below its 100000-node bound; the global time bound was not reached. The JSON includes a checkpoint for every root, counts at every visited length, and an explicit longest extension. Three roots attained length eighteen; all other roots attained at most seventeen. No branch attained length nineteen.

Consequently no endpoint counterexample with four independent tripled elements exists. The same single computation applies to B: its avoidance of zero sums of length <=14 implies avoidance of those of length <=13, and its required length 20 exceeds the computed maximum 18. This is a finite p=5 computation with an explicit capacity dependency on Section 6; it does not extend to other primes.

An independently written C# implementation in `scripts/atom_core_fast.ps1`, mode `four`, subsequently reproduced all 34 roots, 656175 nodes, and every per-root level count, leaf count, maximum length, and completion flag exactly. Its output is `evidence/atom_four_fast_crosscheck.jsonl`, and the machine comparison is `evidence/atom_fast_crosscheck_summary.json`. This is an independent implementation check by the same agent, not a separate-context mathematical audit. In addition, `scripts/atom_verify_longest.py` independently enumerated all 262143 nonempty subsets of one length-eighteen leaf, finding Z_14=39, Z_15=9, Z_16=9 and no other zero sums; see `evidence/atom_four_longest18_graycheck.json`. The latter checks a leaf, not completeness of the search.

## 8. EXACT COMPUTATIONAL EXCLUSION: three tripled elements and an independent doubled element

Suppose S has exactly three distinct elements of multiplicity three. They are linearly independent: if their rank were at most two, their nine terms would contain a zero sum of length at most D(C_5^2)=9. Write H for their rank-three span. If an element of multiplicity two lies outside H, an automorphism normalizes an eleven-position subsequence to

    V=e_1^3 e_2^3 e_3^3 e_4^2.

Every other support element has capacity at most two, by the assumed exact number of tripled elements. This reduction does not require the separate rank-three four-triple proof. Combining this section with a general statement that all bad sequences have at most three tripled elements does require that additional proof as well as Sections 6 and 7.

The same exact distance recurrence and sorted-extension search are used, with cutoff 13 and target 21. The only symmetry is permutation of the first three coordinates, which preserves the core and all capacities. The minimum-orbit argument in Section 7 applies to this S_3 action, with the fourth coordinate fixed. There are 429 safe first additions and 113 canonical first roots. Later additions are unrestricted apart from order, capacity, and the exact zero-sum test.

The Python executable `scripts/atom_three_with_double.py` first completed 86 roots under two bounded runs. The C# executable `scripts/atom_core_fast.ps1`, mode `three_double`, finished the outstanding roots with explicit per-root and whole-run limits. An initial 45-second run with a two-million-node limit completed 23 more roots. Only roots 6, 7, 8, 9 were truncated by that node limit. A further 45-second run with a ten-million-node limit completed all four in 30.49 seconds, using 9623144 nodes in total. No global deadline or node limit truncated a final accepted record.

The merged complete evidence `evidence/atom_three_double_final.json` retains all 113 final records, earlier attempts, and input evidence paths. It reports

    canonical_roots=113
    completed_roots=113
    all_roots_completed=true
    complete_record_node_total=20707001
    maximum_reached_length=18
    terminal_extensions=0.

Thus a sequence with this core and the stated capacities which avoids all zero sums of length at most 13 has length at most 18. Both endpoint counterexamples are excluded. In particular, if a bad endpoint has exactly three tripled elements, **every doubled element lies in H**. This does not exclude that remaining case. This is finite p=5 computational evidence; the fast implementation has been cross-checked on Section 7's complete instance but the whole Section 8 enumeration still awaits a fresh-context audit.

## 9. EXACT FINITE OBJECT: twelve-position hyperplane cores with three tripled elements

Within H=C_5^3, start from e_1^3 e_2^3 e_3^3 and adjoin at most three positions, with capacity two on every new vector, retaining exactly the zero-sum-free extensions. The exhaustive sorted enumeration `scripts/atom_three_hyperplane.py` has level counts

    length 9: 1; length 10: 58; length 11: 738; length 12: 891.

It imposes no symmetry quotient. Every one of the 891 length-twelve extensions is explicitly listed in `evidence/atom_three_hyperplane.json`, together with its shortest-subsequence-distance profile. There are 110 distinct profiles. For every length-twelve sequence V listed:

* every h in H is a subsequence sum;
* exactly one point has distance 12, necessarily sigma(V);
* no point has distance 11;
* at most one point has distance 10;
* at most five points have distance at least 9, and at most two have distance at least 10.

These properties are exact statements about the enumerated normalized cores. This section does not itself conclude that their outside extensions are impossible; the root agent's separate quotient arguments use these properties. Hyperplane intersections of lengths 9, 10, and 11 are not covered by the length-twelve profile assertions.

## 10. EXACT COMPUTATIONAL EXCLUSIONS: double-block cores

Two finite lemmas now hold without an ambient support bound:

1. For any nine distinct elements g_1,...,g_9 of C_5^4, the sequence g_1^2...g_9^2 contains a nonempty zero sum of length at most 13.
2. For any eight distinct elements g_1,...,g_8, the sequence g_1^3 g_2^3 g_3^2...g_8^2 contains a nonempty zero sum of length at most 13.

If the displayed terms span a subgroup of rank at most three, D(C_5^3)=13 proves either statement. For the first lemma in rank four, choose any four independent support elements and normalize their two copies each to e_1^2 e_2^2 e_3^2 e_4^2. For the second lemma, g_1 and g_2 must be independent in a putative counterexample: otherwise their six terms lie on a line, where D(C_5)=5. Extend them to a basis with two of the other six support elements. The normalized core is e_1^3 e_2^3 e_3^2 e_4^2. These reductions impose no restriction on the remaining support vectors beyond distinctness from the basis and one another.

### Exact block rule and symmetry coverage

Let d(h) be the minimum subsequence length as above, and let g^2 be a new double block. A new zero sum uses one or two copies of g. Thus the block is safe at cutoff m exactly when

    d(-g)+1>m and d(-2g)+2>m.

The C# program applies the exact update

    d_new(h)=min(d(h),1+d(h-g),2+d(h-2g)).

It scans all 624 nonzero group elements, excludes the four basis vectors already present, and only adjoins new blocks in strictly increasing encoded order. This excludes duplicate support vectors, as required for the two displayed lemmas. It does not bound coordinates or omit vectors according to a projective normalization.

For the (2,2,2,2) core, the first block is reduced by all S_4 coordinate permutations. For the (3,3,2,2) core, only S_2 times S_2 permutations of the two equal-multiplicity coordinate pairs are used. The first-block coverage proof is the same minimum-orbit argument in Section 7: choose a block whose orbit minimum is least among all blocks, and apply the corresponding automorphism. Every other transformed block has encoding at least that minimum. Later blocks are only ordered, with no further symmetry pruning.

The complete outputs are:

| Basis multiplicities | Cutoff m | Initial safe blocks | Canonical first roots | Complete nodes | Maximum total length |
|---|---:|---:|---:|---:|---:|
| (3,3,2,2) | 14 | 371 | 122 | 22461 | 16 |
| (3,3,2,2) | 13 | 371 | 122 | 24267 | 16 |
| (2,2,2,2) | 14 | 475 | 44 | 183444 | 16 |
| (2,2,2,2) | 13 | 475 | 44 | 185077 | 16 |

Every root completed without hitting its two-million-node or 45-second cap; in fact each complete run used less than one second of search time. No row has a length-eighteen node. This proves the two lemmas, since each displayed sequence would have length eighteen. The searches had target length twenty, which was never reached; the stronger length-eighteen exclusion is visible in their full level counts.

The original B-only executable is `scripts/atom_b_support9_blocks.ps1` with output `evidence/atom_b_support9_blocks.jsonl`. The parameterized executable is `scripts/atom_double_blocks.ps1`; its outputs are `evidence/atom_3322_m13_blocks.jsonl`, `evidence/atom_2222_m14_blocks.jsonl`, and `evidence/atom_2222_m13_blocks.jsonl`. These files retain the full initial safe lists, canonical root lists, every root's completion/level/leaf counts, and a longest branch.

An independently written Python/NumPy implementation, `scripts/atom_verify_double_blocks.py`, reconstructs group arithmetic, explicitly enumerates each symmetry orbit to find its minimum, and adjoins the two copies one at a time using gather updates. It completed all four instances in 9.63 seconds. Every root, node count by length, leaf count by length, total node count, and maximum length matched the C# output exactly. The comparison evidence is `evidence/atom_double_blocks_crosscheck.json`. This is independent implementation verification by this agent, not a fresh-context proof audit.

### Consequences for endpoint multiplicities

Let a,b,c count support elements of multiplicities three, two, and one. Lemma 1 gives a+b<=8 in both bad endpoints, because two copies can also be selected from a tripled element. Lemma 2 gives a+b<=7 when a>=2. The later leaf certificates in Section 13 strengthen the uniform bound to **a+b<=7**, and Section 14 excludes the case a=2,b=5. In the exactly-three-tripled case, Section 8 puts every doubled element in their rank-three span H, whose intersection with a bad sequence has length at most twelve. Therefore 9+2b<=12 and **b<=1**.

Conditional on the separate rank-three four-triple exclusion (together with Sections 6 and 7), a<=3, so the current support consequences are:

| Number a of tripled elements | Largest possible b | Minimum A support | Minimum B support |
|---:|---:|---:|---:|
| 0 | 7 | 14 | 13 |
| 1 | 6 | 13 | 12 |
| 2 | 4 | 13 | 12 |
| 3 | 1 | 14 | 13 |

Here c=N-3a-2b and support=N-2a-b. Consequently A has support at least thirteen and B at least twelve, with the stated dependency on excluding four tripled elements. This finite reduction does not exclude the remaining higher-support sequences.

## 11. BOUNDED INCOMPLETE OBJECT: H has eleven positions and outside positions are distinct

For the remaining exactly-three-tripled class, the preparation `scripts/atom_h_core_prepare.py` enumerates all zero-sum-free eleven-position H cores consisting of e_1^3 e_2^3 e_3^3 and two added H positions. There are 738 raw extensions and 131 S_3 orbits. Each orbit size is checked against its six explicit coordinate permutations. The full list is `evidence/atom_h11_cores.json`; the later profile-enriched copy is `evidence/atom_h11_core_profiles.json`.

For each H core one arbitrary outside position can be normalized to e_4 by an automorphism fixing H pointwise. Every other outside vector still has nonzero fourth coordinate and therefore a base-five encoding at least 125. This is a consequence of being outside H, not an additional minimum-choice assumption. The fixed e_4 has encoding 125 and cannot be reused, because outside positions are distinct by Section 8. The remaining outside universe is exactly the vectors 126,...,624, filtered only by the zero-sum criterion.

The bounded executable `scripts/atom_h_outside_fast.ps1` was run at cutoff 13 with target 21, a 45-second overall deadline, and two million nodes per H core. Its output `evidence/atom_h11_probe.jsonl` completes 13 of the 131 cores, with maxima at most 17. A fourteenth core, id 38,108, was interrupted by the overall deadline after 21504 nodes. Total visited nodes were 13116309. This output is explicitly **INCOMPLETE**; the other 118 cores have not received completed records, and no general H=11 exclusion follows.

The small-core distance profiles are complete, independent of that outside search: coverage |Sigma(V)| is at least 100, the number of unreachable points is at most 25, and the maxima of |{h:d(h)>=k}| for k=8,9,10,11,12 are respectively 33,29,27,26,25. These counts include unreachable points as infinite distance. All 131 full distance tables are stored and represent all 738 raw cores under the orbit action. The larger exceptional sets explain why the twelve-position profile criterion cannot simply be reused unchanged.

## 12. CERTIFIED OBSTRUCTION to strengthening the double-support bound

The last bounded block check asks whether one tripled element and seven further doubled elements already force a zero sum of length at most 13. They do not. Normalize the core to e_1^3 e_2^2 e_3^2 e_4^2 and append four distinct double blocks, with only S_3 permutations of coordinates 2,3,4 used for the first block. The program `scripts/atom_one_triple_blocks.ps1` completes all 106 canonical roots among 430 initially safe double blocks. It visits 121866 nodes and finds 428 length-seventeen terminal branches. The complete evidence is `evidence/atom_3222_m13_blocks.jsonl`; these terminal branches are not claimed to be inequivalent under all automorphisms.

One explicit seventeen-position survivor is

    e_1^3 e_2^2 e_3^2 e_4^2
    (1,1,0,0)^2 (3,1,1,0)^2 (3,1,1,1)^2 (4,2,4,1)^2.

The independent coefficient enumerator `scripts/atom_3222_certificate.py` checks every one of the 4*3^7=8748 bounded coefficient tuples. Weighting each tuple by the appropriate binomial coefficients covers all 2^17 position subsets. It finds precisely six nonempty zero-sum position subsets, all of length fifteen. Thus Z_15=6 and every other nonempty Z_k is zero. The full vector list, multiplicities, and every zero-sum coefficient tuple are in `evidence/atom_3222_length17_certificate.json`.

Accordingly, the proposed strengthening a+b<=7 merely from a>=1 is false for the short-zero-sum condition on arbitrary subsequences. This does not prove such a seventeen-term survivor can extend to either endpoint length, and it is **not an A or B counterexample**. The separate NumPy/gather check `scripts/atom_verify_one_triple_blocks.py` subsequently reproduced all 106 roots, all per-length node and leaf counts, and all terminal counts exactly in 1.78 seconds; see `evidence/atom_3222_crosscheck.json`.

## 13. COMPLETE LEAF CERTIFICATES and their endpoint consequence

The following computations only revisit leaves of already complete block trees. They do not start a general suffix search. The original programs and outputs were preserved; new callbacks use `scripts/atom_double_block_leaf_profiles.ps1` and `scripts/atom_3322_leaf_profiles.ps1`.

### The 428 seventeen-position survivors cannot accept even one additional position

For every length-seventeen (3,2,2,2) leaf in Section 12, all 625 group points are attained. The maximum shortest-subsequence distance is eight at 141 leaves, nine at 189 leaves, and ten at 98 leaves. Hence every group element g has d(-g)<=10, and adjoining any g creates a zero sum of length at most eleven. The full leaf profiles and the complete empty safe-addition lists are in `evidence/atom_3222_leaf_profiles.jsonl`.

Thus the seventeen-position certificate remains a valid obstruction to the shorter standalone statement, while **no sequence of length at least eighteen avoiding zero sums of length at most thirteen can contain a tripled element and seven further distinct doubled elements**. If those terms span rank at most three, the Davenport bound already excludes them. Otherwise the tripled element can be included in a basis chosen from their support, so the complete normalized leaf list applies.

### Every safe sixteen-position double core has at most one admissible next value

The complete (2,2,2,2), cutoff-thirteen tree has exactly 10196 length-sixteen leaves, representing eight distinct support elements with two copies each. All 625 group points are attained at every such leaf. Define

    A(W)={g in C_5^4 : Wg contains no nonempty zero sum of length <=13}.

Exactly 2153 leaves have |A(W)|=0 and 8043 have |A(W)|=1. The maximum-distance distribution is

    9:859; 10:346; 11:712; 12:236; 14:495; 16:7548.

Every safe value is explicitly listed in `evidence/atom_2222_leaf_profiles.jsonl`. No unlisted value is omitted by a capacity or distinctness filter: the callback tests all 625 group elements, including values already in W.

Suppose a bad endpoint S contained eight support elements of multiplicity at least two. Select their sixteen-position double core W. Rank at most three is impossible by D(C_5^3)=13, so W has one of the normalized leaf profiles. Every remaining position of S must individually belong to A(W), because W together with that position is a subsequence of S. If A(W) is empty there is an immediate contradiction. If A(W)={g}, all N-16 remaining positions equal g. Since N>=20, S contains at least four copies of g, contradicting the proved height bound h(S)<=3. Consequently **both bad endpoints satisfy a+b<=7**. This argument needs no enumeration of possible later suffixes.

### The two-tripled/five-doubled leaves require a further finite check

The complete (3,3,2,2), cutoff-thirteen tree has 15684 length-sixteen leaves. Their safe-addition cardinalities are

    0:977; 1:3970; 2:3012; 3:801; 4:6316; 5:604; 6:4.

Twelve leaves attain only 623 group points; all other 15672 attain every point. All safe values, including values already present, are listed in `evidence/atom_3322_leaf_profiles.jsonl`. The leaf histogram alone does not justify replacing a+b<=7 by a+b<=6 in the two-tripled case. The bounded four-subset check in Section 14 resolves the relevant endpoint suffixes; no unrestricted suffix tree was run.

### Completeness and independent checks

For each of the three callbacks, the root set and node counts at every length agree exactly with the already completed source tree. The count of profile records at every root equals the source tree's count at the designated leaf length. For the two length-sixteen callbacks, the original complete tree has no longer block extension, so those nodes are precisely its length-sixteen leaves. All recorded block tuples are distinct as encoded tuples; no claim of inequivalence under the full automorphism group is made.

The separate NumPy programs `scripts/atom_verify_leaf_profiles.py` and `scripts/atom_verify_3322_leaf_profiles.py` rebuild the subsequence-distance table for every listed leaf, check the saved distance histograms, all safe-addition vectors, and the leaf denominators against the preserved original tree. All comparisons pass. Their summaries are `evidence/atom_3222_leaf_profiles_check.json`, `evidence/atom_2222_leaf_profiles_check.json`, and `evidence/atom_3322_leaf_profiles_check.json`.

## 14. EXPLICIT FINITE CERTIFICATES: two tripled, five doubled, and four single elements

Every twenty-position sequence with multiplicity pattern (3^2,2^5,1^4), on eleven distinct support elements, contains a nonempty zero sum of length at most thirteen.

To prove this, select its sixteen-position core W formed by the two tripled and five doubled elements. If W has rank at most three, D(C_5^3)=13 applies. If its two tripled elements are dependent, their six positions on a line already contain a zero sum of length at most five. Otherwise in rank four choose the two tripled elements and two of the doubled elements as a basis, so W is one of the complete normalized length-sixteen leaves of the (3,3,2,2) tree. Each of the four remaining elements is outside the support of W, they are pairwise distinct, and each must belong to A(W) individually in a putative counterexample.

After filtering each saved leaf's safe list by the support of W, the number of outside-safe values has the distribution

    0:3380; 1:3110; 2:1894; 3:863; 4:5879; 5:554; 6:4.

There are precisely 6437 leaves with at least four such values. The total number of four-subsets to check is

    5879*C(4,4)+554*C(5,4)+4*C(6,4)=8709.

The executable `scripts/atom_3322_outside_micro.py` first computed this exact denominator and refused to proceed if it exceeded its 100000-combination cap. It then checked all 8709 four-subsets, producing a concrete zero-sum subsequence of length at most thirteen for each. Every check and its zero-based position indices in the corresponding twenty-position sequence are stored in `evidence/atom_3322_outside_micro.json`. No four-subset survived.

The separate verifier `scripts/atom_verify_micro_witnesses.py` uses only plain integer coordinates: it checks that the stored four-subsets equal all four-subsets of all saved outside-safe lists, with no duplicates, and directly sums each claimed zero-sum witness modulo five. It does not use a distance DP or perform a search. All 8709 witnesses pass; their length distribution is

    5:184; 6:671; 7:1777; 8:2524; 9:2202; 10:966; 11:324; 12:49; 13:12.

The verifier summary is `evidence/atom_3322_outside_micro_check.json`. The four-subset enumeration took 2.02 seconds. This closes the exact B multiplicity pattern (a,b,c)=(2,5,4). It also closes A's (2,5,5), since selecting any four of its five single elements yields one of the excluded twenty-position subsequences.

With the separately established a<=3 classification, the uniform a+b<=7 bound, and the a=3 implication b<=1, this strengthens the remaining multiplicity condition to **a>=2 implies a+b<=6**. The finite pattern theorem itself only uses the normalized core computation, the leaf completeness/profile certificates, and the explicit 8709 zero-sum witnesses; its statement does not depend on the external four-triple proof.

## 15. Exact remaining patterns and dependency boundary

Combining this route with the root agent's rank-three four-triple proof as an explicit external dependency, every remaining bad sequence has height at most three and a<=3. For a<=2 the remaining multiplicity patterns are exactly the following candidates allowed by the present multiplicity bounds; their listing does not claim realizability:

| Endpoint | Tripled a | Doubled b | Single c |
|---|---:|---:|---:|
| A | 0 | 0,...,7 | 21-2b |
| A | 1 | 0,...,6 | 18-2b |
| A | 2 | 0,...,4 | 15-2b |
| B | 0 | 0,...,7 | 20-2b |
| B | 1 | 0,...,6 | 17-2b |
| B | 2 | 0,...,4 | 14-2b |

All still have to satisfy full rank, the line and plane occupancy restrictions, and the atom-complement conditions. This route has not exhausted any entire row.

For a=3, let H be the span of the three tripled elements and write n_H=|S intersect H|, counting positions. Section 8 forces every doubled element into H, and D(H)=13 forces n_H<=12. The possibilities with n_H=9,10,11 are therefore exactly:

| n_H | Doubled b | Further single positions inside H | Distinct outside positions in A | Distinct outside positions in B |
|---:|---:|---:|---:|---:|
| 9 | 0 | 0 | 12 | 11 |
| 10 | 0 | 1 | 11 | 10 |
| 11 | 0 | 2 | 10 | 9 |
| 11 | 1 | 0 | 10 | 9 |

The n_H=11 row is only partly searched as recorded in Section 11. No complete outside search has been performed here for n_H=9 or 10. The remaining n_H=12 possibilities have (b, further H singles)=(0,3) or (1,1); their profile assertions are certified in Section 9. Excluding their outside extensions is the separate root-agent quotient proof, not a conclusion of the computations in this file. Until that proof has passed its own audit, n_H=12 remains an explicit conditional exclusion rather than a closed case in this route.

The remaining a=1,b=6 case was examined only through nodes of the already completed (3,2,2,2) block tree. There are exactly 107656 length-fifteen nodes, representing one tripled and six doubled support elements. A new callback in `scripts/atom_3222_len15_scan.ps1` scans their safe single additions outside the core support, without extending any node. Every root completed, and the node counts through length fifteen match the earlier complete tree. The output `evidence/atom_3222_len15_scan.jsonl` records the complete safe lists and the following outside-candidate counts:

    0:2714; 1:6426; 2:5430; 3:6873; 4:7338; 5:4743;
    6:7006; 7:16801; 8:6864; 9:5200; 10:10975; 11:6361;
    12:7596; 13:4503; 14:4898; 15:1595; 16:1381; 17:341;
    18:443; 20:159; 127:9.

The exact total number of five-subsets of these candidate lists is 2336039691. Nine exceptional nodes with 127 candidates contribute 2288085975 of these combinations; the other nodes contribute 47953716. The independent NumPy reconstruction `scripts/atom_verify_len15_scan.py` rebuilt all 107656 distance profiles, checked every safe/outside-safe list, matched the original tree's root denominators, and recomputed the integer combination total; see `evidence/atom_3222_len15_scan_check.json`. This exceeds the intended micro-combination scope, so **zero five-subsets were enumerated**. The standalone finite pattern (3,2^6,1^5) of length twenty remains unresolved by this route. It is not legitimate to infer an exclusion from its initial safe-list scan.

No new searches are running. Further work must address these exact higher-support or smaller-hyperplane configurations rather than reusing the eliminated high-multiplicity cores.

## 16. Exact breakpoint

No contradiction has been obtained here for all actual C_5^4 sequences with multiplicities at most three and at most three tripled elements, or for the separate rank-three case of four tripled elements assigned to the root agent. For exactly three tripled elements, the remaining class has all doubled elements in their span H, and every outside position has multiplicity one. Sequences with at most two tripled elements remain outside these core exclusions. They must also satisfy the displayed subspace restrictions and atom-complement covering bounds. The remaining difficulty is a realization restriction on these smaller-multiplicity configurations; the finite core computations do not exhaust them.

The canonical 15-atom

    e_1^3 e_2^3 e_3^3 e_4^3 (e_1+e_2)(e_3+e_4)(e_1+e_2+e_3+e_4)

shows why it would be invalid to assert that every 15-atom has a term of multiplicity four. To check minimality, let x,y,z in {0,1} indicate the last three terms. The first pair of basis multiplicities must be [-x-z]_5 and the second pair [-y-z]_5. If z=0, nonzero x or y would require multiplicity four; if z=1, both x and y must equal one, forcing all four basis multiplicities to be three. Thus the only nonempty zero sum is the entire 15-term sequence. This example is not a counterexample to A or B, because it has only 15 terms.

Final status for A and B remains **INCOMPLETE**. No statement of novelty or exact K(C_5^4) is made.
