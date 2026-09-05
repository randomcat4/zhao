# Exact search route

STATUS: **INCOMPLETE** for A and B. No counterexample and no full-family exclusion was obtained. The saved spectra below are exact; failure of the randomized searches is not evidence of a theorem.

The work directory was C:/game/gameproject/showa100. This route did not access C:/canglan, start Euler, spawn agents, or use paid external computation. It read the frozen theorem and previous structural report before receiving the parent agent's directed multiplicity-bound update. It did not read other current-round route drafts.

## New exhaustive object

The exact computation in `../scripts/search_support7_cap3.ps1` establishes the finite statement:

> For any six distinct nonzero elements g1,...,g6 of C5^4, the sequence g1^3 ... g6^3 has a nonempty zero sum of length at most 13.

If their rank is at most three, the supplied Davenport bound D(C5^3)=13 gives this directly. In rank four, choose and send four independent elements to the standard basis. The remaining two columns a,b are an unordered pair among the 620 vectors different from zero and the four basis vectors. Thus there are exactly binom(620,2)=191890 normalized matrices.

With all multiplicities equal to three, every permitted zero sum has coefficients

    ([-t*a1-u*b1]_5, ..., [-t*a4-u*b4]_5, t, u),
    t,u in {0,1,2,3}, (t,u) != (0,0),

where each of the first four entries must also be at most three. The script checks every such coefficient vector, using exact integer arithmetic. Its completed output in `../evidence/search_support7_cap3.log` is:

    FINAL pairs=191890 surviveA=0 surviveB=0 candidatesA=0 candidatesB=0 badA=0 badB=0 ms=52

No seventh-column enumeration was necessary: every six-column prefix of multiplicities 3 already failed avoidance of length <=13. The script name reflects the initially intended extension. This calculation was sent to the structural route as soon as the overlap in assignments was discovered; this route then stopped that enumeration work.

A consequence that applies at **every support size** is:

    #{g : multiplicity_S(g) >= 3} <= 5

for either bad endpoint sequence. Otherwise take three copies each of six such elements and apply the checked statement. This implication does not need a separate bound of three on all multiplicities. Combined with a proved maximum multiplicity of three, it would imply support >=8 at both endpoints, since |S| <= 2*|support(S)|+5. The parent agent is responsible for the independent verification of the newly supplied multiplicity-three bound and this finite computation. This route does not claim formal verification or a general-prime analogue.

## Search representation and exact update formulas

A group element is encoded as

    code(x1,x2,x3,x4) = x1 + 5*x2 + 25*x3 + 125*x4,
    0 <= xi <= 4.

The four fixed positions have codes 1,5,25,125. Every full-rank sequence can be put in this form by choosing four independent positions and applying an invertible linear map. No translation was used. Each unfixed position can take all 624 nonzero values in `full` mode, subject only to the logged multiplicity cap.

`affine` mode allows the 125 values satisfying x1+x2+x3+x4=1 mod 5. Every zero sum in this family has cardinality divisible by five. Thus at the B endpoint the forbidden lengths are exactly 5 and 10. Fixing the four standard basis positions still loses no full-rank member of the affine family: after a linear normalization, the defining linear functional takes value one on each standard basis vector and hence is their coordinate sum. This family is not all of C5^4.

For a current sequence S, let D_k(g) count indexed subsets of cardinality k and sum g. Initially D_0(0)=1. Inserting x changes

    D'_k(g) = D_k(g) + D_(k-1)(g-x).

Deleting one occurrence of x can be computed exactly, in increasing k, from

    Q_0 = D_0,
    Q_k(g) = D_k(g) - Q_(k-1)(g-x).

Replacing that occurrence by y therefore gives, for every k,

    Z'_k = Q_k(0) + Q_(k-1)(-y).

This evaluates all legal replacements without enumerating 2^N subsets at each local-search step. At N<=21 all counts fit safely in 32-bit signed integers, since even the sum of all subset counts is at most 2^21. All search decisions may be heuristic, but every logged spectrum is produced by exact counts.

`search_local.ps1` minimizes sum w_k*Z_k. We used unit weights, then w_k=2^(m-k) or 8^(m-k). These are exploratory objectives only. `search_lex.ps1` instead compares the full integer vector (Z_1,...,Z_m) lexicographically, thereby prioritizing the shortest zero-sum length and then its count. Both include random restarts and explicitly logged perturbations. Candidate replacements and sequences can repeat; the reported evaluation totals are not counts of distinct sequences.

`search_grow.ps1` is a separate algorithm. It maintains the minimum cardinality reaching each group sum and adds x only if no current subset of length <=m-1 sums to -x. Consequently every retained partial sequence has no zero sum of length <=m. When no extension exists, it removes random unfixed positions and regrows. This remains a randomized search, not a complete backtracking enumeration.

## Completed local-search budgets

The eight fixed-length runs made **1,587,268,556** exact replacement-spectrum evaluations in total.

| Endpoint / domain | Cap | Objective | Seed | Restarts x steps | Evaluations | Best shortest zero |
|---|---:|---|---:|---:|---:|---:|
| B / affine | 4 | unit weights | 104729 | 30 x 3000 | 11,075,670 | 5 |
| A / full | 4 | unit weights | 104723 | 30 x 3000 | 55,816,586 | 2 |
| B / affine | 4 | base 2 | 99991 | 150 x 3000 | 55,176,413 | 10 |
| A / full | 4 | base 2 | 99989 | 150 x 3000 | 279,026,654 | 9 |
| B / affine | 3 | base 8 | 982451653 | 200 x 4000 | 97,527,357 | 10 |
| A / full | 3 | base 8 | 961748941 | 200 x 4000 | 495,529,194 | 9 |
| B / affine | 3 | exact lexicographic | 15485867 | 200 x 4000 | 97,432,364 | 10 |
| A / full | 3 | exact lexicographic | 15485863 | 200 x 4000 | 495,684,318 | 10 |

The multiplicity cap 3 was introduced only after the parent supplied its new structural route result. The cap-4 runs retain the weaker original constraints. No result from a cap-3 search by itself establishes that cap 3 is sufficient for exhaustive coverage.

Each growth run used 500000 iterations. Full A (seed 32452843) made 312000000 domain membership tests and 377681 accepted extensions; affine B (seed 32452867) made 62500000 domain membership tests and 377261 extensions. Both reached length 17. The future-option lookahead is additional heuristic work, not included as an exhaustive-case count.

## Exact retained sequences

The best shortest-zero length reached for full-domain A, under cap 3, was 10. Its complete sequence is

    1,5,25,125,581,65,581,5,90,190,46,125,581,190,210,541,190,541,5,90,601

and its complete nonempty zero-sum spectrum is

    10:12, 11:1455, 12:1425, 13:1400, 14:1300, 15:63, 16:55.

For affine B under cap 3, a retained best sequence is

    1,5,25,125,1,170,25,25,46,125,46,46,5,125,170,591,5,170,1,206

with spectrum

    10:270, 15:216.

Neither is a counterexample. The full-domain growth search produced this length-17 sequence avoiding <=13:

    1,5,25,125,509,348,389,439,179,222,537,171,342,25,171,25,171

with spectrum `14:3,16:1`. The affine growth search produced this length-17 sequence avoiding <=14:

    1,5,25,125,190,190,25,125,25,5,1,1,5,190,125,543,543

with spectrum `15:6`. These are only lower-bound witnesses at length 17.

## Independent arithmetic verification

`../scripts/search_verify.py` independently materializes the four-coordinate residue sum and cardinality of **every indexed subset** of each saved final sequence. It does not reuse the 625-state DP recurrence or its group-addition tables. All ten final sequences passed this check. Their full coordinates, rank, multiplicities, spectra, and one indexed witness for each nonempty zero-sum length are saved in `../evidence/search_independent_verification.json`.

The verifier enumerates 2^20 or 2^21 subsets for the fixed-length sequences, and 2^17 for each growth witness. It checks exact equality with the spectra in the original logs. This is independent arithmetic implementation, not a fresh-agent logical audit or a Lean certificate.

## SAT formulation and exact remaining obstruction

`../scripts/search_sat_lazy.py` supplies a complete Boolean multiplicity representation for the selected domain and cap. The Boolean x[g,r] means multiplicity(g)>=r; monotonicity and an exact cardinality constraint enforce a length-N multiset. The four standard basis values must appear. In affine B with cap 3 this uses 125*3=375 Boolean variables.

Whenever exact indexed-subset enumeration finds a short-zero multiset a, the script adds the globally valid clause

    OR over g in support(a) of NOT x[g,a(g)].

Every model of the intended avoidance problem satisfies every such clause. Hence UNSAT of even a finite set of these valid clauses would exclude the entire normalized selected family. A SAT model is accepted only after exact enumeration finds no forbidden subset. Ordinary SAT models before that check are not counterexamples. Saved `.cuts.jsonl` files expose every generated zero multiset for separate validation.

The completed first run is affine B, cap 3, seed 17, with a 120-second wall-clock budget. It ended **INCOMPLETE**, with Z3 reporting `canceled` when the wall-clock allowance expired. There were 121 solver checks, of which the last timed out, and 68994 saved valid cuts. No final counterexample or UNSAT certificate exists. Its authoritative output is `../evidence/search_sat_affine20_17.result.json`. `../scripts/search_audit_cuts.py` checks every saved cut directly as a nonempty zero-sum multiset of forbidden length; its output is `../evidence/search_cut_audit.json`. Z3 5.1.0 was installed only into this run's `local_deps/search_z3` directory. No global environment was modified.

The remaining gap is still a global exclusion or a valid sequence at either endpoint. The searches cover elements at arbitrary support sizes, but their bounded randomized evaluations and the incomplete SAT run do not establish either frozen statement.
