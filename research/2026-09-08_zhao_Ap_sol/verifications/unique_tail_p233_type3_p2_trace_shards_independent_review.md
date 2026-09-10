# `p=233` type-`(3)`, `|P|=2` outer trace shards: independent review

STATUS: **CORRECT**

Date: 2026-09-09

## Frozen inputs

This review is bound to exactly these three author artifacts:

- `unique_tail_p233_type3_p2_trace_shards.py`
  SHA-256 `8491c8cb872f588413634d2858019102721b925c6fc59005b5f3e535bcb5085c`
- `unique_tail_p233_type3_p2_trace_shards_report.json`
  SHA-256 `63a11953d8d8be06832d2464f8b4c021abd822d457f5d7ef4b1ebef55c7f6065`
- `proofs/unique_tail_p233_type3_p2_trace_shards.md`
  SHA-256 `afb51b5b795112ec851305613ce8ac467ca78f2a4c8c23104e84767e8954b78f`

The independent enumerator used for this review did not import or execute the
author module.

## Independent graph enumeration

I generated every labeled simple graph with exactly four edges and no isolated
vertices, for vertex counts four through eight, and canonicalized each graph
over all vertex permutations.  This independently produced eleven isomorphism
classes, distributed by vertex count as

\[
2,\ 4,\ 3,\ 1,\ 1.
\]

Their component/degree structures agree exactly with the eleven representatives
listed in the script and proof:

\[
P_5,K_{1,4},T_5,C_4,\mathrm{paw},
P_4\dot\cup K_2,K_{1,3}\dot\cup K_2,K_3\dot\cup K_2,
2P_3,P_3\dot\cup2K_2,4K_2.
\]

Every representative has four distinct simple edges, uses every declared
vertex, and is isomorphic to one and only one independently generated class.

## Independent trace enumeration

The six nonempty proper traces of a three-position tail were represented by
the masks `1,...,6`.  I independently enumerated all `6^s` assignments on each
of the eleven fixed graph representatives and retained exactly those for which
the two endpoint masks of every edge have bitwise-disjoint support.

The resulting totals are

\[
28{,}584=28{,}548+36,
\]

where 28,548 assignments repeat at least one endpoint trace and 36 assignments
are injective.  The only graph shapes with nonzero injective count are

| Shape | Injective assignments |
|---|---:|
| `paw` | 6 |
| `P5` | 6 |
| `T5` | 12 |
| `P4_plus_K2` | 12 |

These values agree entry by entry with the report's full eleven-shape count
table.  Each injective assignment contains all three singleton masks `1,2,4`.
This also follows directly from the six-trace disjointness graph: deleting any
singleton vertex leaves only three available disjointness edges, whereas the
outer graph has four distinct edges.

## Report row audit

All 36 `trace_shards` rows were checked individually.  For every row:

- `vertex_count` agrees with the named fixed representative;
- the edge list has four distinct simple edges, stays in range, and has no
  isolated declared vertex;
- the trace-mask list has the declared length, uses only masks `1,...,6`, is
  injective, contains `1,2,4`, and is disjoint along every listed edge;
- the `(shape, endpoint_trace_masks)` pair belongs to the independently
  regenerated exhaustive injective set.

Conversely, every independently regenerated injective assignment occurs once
in the report.  There are no missing or duplicate shards.  Rows are in exact
lexicographic order by shape name and trace tuple, and `shard_id` is precisely
`trace-01` through `trace-36` in that order.  Thus the numbering is stable under
the stated v1 ordering rule.

The report certificate
`2e15c4f39374da1f5cc78f12284b852998715f28246fd87becc6ea640120448d`
recomputes correctly from the report after removing the certificate field.

## Scope and status

The script, report, and proof consistently freeze the local slice

\[
p=233,\quad (\ell,b)=(7,4),\quad \text{type }(3),\quad
|P|=2,\quad \kappa=1,
\]

with length-seven endpoints and rank-two tail projection.  They make only an
outer combinatorial exhaustion claim: one representative of each four-edge
no-isolated graph type, followed by every injective six-trace assignment on
that representative.  They explicitly do not quotient by graph automorphisms
or tail-coordinate permutations; retaining equivalent shards can duplicate
later work but cannot omit a branch.

The boundary language is accurate.  No endpoint mask in the shared 474-row
`Y`, quotient label, height, short-block family, Hasse certificate, or atom
oracle result is supplied.  The artifact therefore does not claim a complete
incidence enumeration, `SAT`, `UNSAT`, a fixed-prime counterexample, or the
global endpoint theorem.  Its status correctly remains

`EXACT_OUTER_TRACE_PARTITION/36_SHARDS/INCIDENCE_AND_LABELS_PENDING/GLOBAL_INCOMPLETE`.

## Verdict

The eleven graph representatives and their six-trace assignments are
exhaustive at the stated outer boundary.  The total count, repeated/injective
split, four surviving shapes, per-shape shard counts, every saved row, stable
identifier order, certificate, and incompleteness wording all passed fresh
independent verification.  No critical gap or false global claim was found.
