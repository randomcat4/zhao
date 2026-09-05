# GitHub upload scope

This directory is the reviewable text/source subset uploaded through the GitHub connector. The local certificate bundle also contains large generated evidence and a binary ZIP that are not represented here byte-for-byte.

Included here are the self-contained proof, red-team report, integer branch schema, exact Farkas certificate, root generator, reference extension search, independently implemented extension verifier, interface/legacy/negative-control checkers, unit checkers, replay driver, result/coverage summaries, provenance, and execution summary.

The local full bundle `PRO_SF2_dense_fibre_certificate.zip` has SHA-256

`54ed47aba222d9b5e6da43a861a9ac496966074d5d1b439c7e63e318f3a08dfb`.

Not uploaded byte-for-byte in this connector pass: the 1.4 MB row-expanded `m_coverage.csv`, the 38 KB generated `rank3_roots.txt`, and the large per-root raw search logs. Their exact denominator information is retained in `RESULT.json`, `m_coverage_summary.csv`, `verify_logs.log`, and `proof_zh.md`. The source tree still includes the root generator and independent orbit verifier; a future byte-for-byte artifact upload should preserve the local bundle hash above rather than inventing a substitute hash.

Because `run_all.py` in this review copy is the archival replay driver from the full local bundle, it expects the generated/fixed root table used by that bundle. Absence of a large generated file from this connector upload must not be interpreted as a successful replay. The mathematical terminal label should be assessed from the proof plus the complete local certificate or a genuinely complete regeneration.
