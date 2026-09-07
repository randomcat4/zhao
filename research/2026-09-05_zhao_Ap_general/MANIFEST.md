# Archive manifest

This directory is a curated repository archive of six research packages produced in the thread. Large duplicate input notes and transient logs were not copied; each later verifier wrapper or note points to the earlier round's canonical files in this directory tree.

The `verify_src/` files in rounds 1--4 preserve the substantive verifier source in ordered parts. The small top-level verifier wrappers concatenate those parts. Round 2 and round 4 wrappers replace only the original duplicated-input path with the canonical previous-round note path. Round 3 and round 4 wrappers materialize the concatenated source temporarily because the original verifier records its own source hash.

Round 5 is appended as a direct self-contained package (`research_note.md`, `verify.py`, `verification_report.json`). Its verifier was independently written and run before archival; it checks the explicit `x_0=0` construction, point/pair/vector identities, deletion orbits, finite cross-pair regressions, and structural arithmetic. It is not an `A_p` verifier and does not certify `h(S)<=p-5`.

Round 6 is a correction/self-audit package (`research_note.md`, `AUDIT.md`, `verify.py`, `verification_report.json`). It retracts the continuation shortcut `theta=-1 => sigma(R)=0`, records the correct value `Lambda_i=0 in F_p`, and archives the integer-unimodular over-deletion transform. It keeps the strict theorem at `h(S)<=p-4` and states length control for the top complement `U` as the next open step.

Original/local-package SHA-256 values before curation or append:

| round | research note | verifier | full/generated report | audit / auxiliary |
|---|---|---|---|---|
| 1 | `3ac154b21bb4957ca03954a885d202a98b9bb250596786a1d78699eea93f3d3a` | `0bf317dfd87a35e1b72545b3f1d1ac62cc5eef99678e8e5a639cdd458e74e200` | `7bfcf3de5e397a6e5ea411d97e3cb92ae0a9fe55c27a94687dd19eaa09f47ea6` | audit `524bd5b537257f8526aaf335bf5fc6baac7654ea8540fbaec9fe34ee51731082` |
| 2 | `83bdb30a4d0e0cac776c18a21cb362f5b787fb505508caa5145a4195bd7e4462` | `576a5dc1579d373b92a5f1613d3a5fcc2b706711e4b3479933bf44861e8a66d8` | `5cbe2aa41c6dda1bfe6bf899e5b5c868227f66b52a7f930fcd7ebee243e983fa` | `symbolic_interfaces.json` `af0a0a648222527558deb5d83c85f6625aea2e324cb2b5637d6fd5ea2d0b428a` |
| 3 | `b09f4d0e98a3d7cac1c72b48cb39714f8758e3a9bd0b4f4a8f1f8b73d4d8fffa` | `bf52b24e8f5dc0004dce277e9571a50233f99adc8a7a6f2bf1781fa0d3138f0d` | `ce3fc76802a3165c95886202394c79c4af56a47f826c2122a4a443e13e0e0510` | audit `439af09c7ad2aab17bd95a7b515e5070c7ec69402ba50da3e5346835de3bec8f` |
| 4 | `ed3e3c70a08fae4acac5bc5a2b94ba7a5da9a4c4471a315fd8c12ee1403c147d` | `504cb96943788d52c35c1c8dbbfbf313d407da5a3e81546147950a9ad840a691` | `da153632715c1f0eeb703adba04b83e83b730b18c4f9976524eefa98a89e64fb` | audit `ba098691e23330fc744ee6ddde24bc6aa0eaace23d69b2ef49957d081a691572` |
| 5 | `1765a2ccdbf700ff1ae7ce716581629da613d5fb4fc4fa246fd78aa1a122450e` | `4222e10ea33221f33df46cd02f2206529fc76f1ff0258f6b6ed6653c3ed1ceed` | `4f2b202357ee5a1f12e3de6ab58dfb40ee9ff72b71cae9b131ee284bc5d77987` | self-contained append; no separate audit file |

Round 6 was appended directly to the repository branch, so the stable identifiers recorded here are Git blob SHAs rather than local-package SHA-256 values:

- `research_note.md`: `ce9b13dbbaa6212be5b992f99e82bd96cdbde9fa`
- `AUDIT.md`: `e83656f71fac611b833aa5e7e1cb882aa7f91e0e`
- `verify.py`: `9fe4cf370ea3d83e81288a1f2acb13c1ac580771`
- `verification_report.json`: `16998a39717ddfa4d82ab2d65d8e1588ca7dfe98`

The first four original verifier entry points were replayed successfully immediately before the original archive was prepared. Round 5's verifier was executed independently before append. Round 6's exact arithmetic verifier was executed before archival; it checks `r=4,...,20` and is not a sequence enumerator.

No archive file changes the mathematical status: full `A_p` is still open in this research thread; the strongest unconditional theorem archived here remains `h(S) <= p-4` for any hypothetical counterexample. Round 6 explicitly prevents the retracted shortcut from being reused and replaces it with the top-complement/over-deletion mechanism.
