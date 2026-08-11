# 京张城市完整度 / JING-ZHANG CITY COMPLETENESS — Continuation Handoff

> Purpose: persistent handoff for future ChatGPT/project conversations. Read this file first before continuing finalization or upstream submission work.

## Working target

- Fork: `miyuuteshima984/haidian`
- Formal working branch: `submission/miyuuteshima984/jingzhang-ai-civic-infrastructure`
- Formal package: `submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure/`
- Same-fork diagnostic PR: `miyuuteshima984/haidian#2`
- Diagnostic branch: `validation/miyuuteshima984/jingzhang-ai-civic-infrastructure`
- Upstream target: `open-city-ai/haidian:main`
- Do **not** treat diagnostic PR #2 as the official upstream submission PR.

## Last recovered conversation checkpoint

The previous long conversation stopped at internal step **7e-4a**. At that point the plan was to retrieve the remaining seven PNG binaries, verify Git blob SHA-1, and calculate SHA-256 before touching the manifest. That was a workaround for truncated binary/base64 output from the GitHub connector.

After re-reading the repository's canonical tooling, that workaround is **not required for finalization**. `scripts/finalize_submission.py` reads the complete local file bytes itself and computes SHA-256. Therefore do not manually guess or paste PNG SHA-256 values into the final manifest.

## Confirmed completed work

- Chinese-primary bilingual formal proposal exists.
- 13 mandatory formal-section headings were aligned between Chinese and English.
- Five required bilingual core figure pairs exist.
- Bilingual report HTML, offline visual pages, A3 booklet and A0 boards exist.
- Nine required GeoJSON layers exist.
- `constraints.geojson` is intentionally empty and documented as a real data gap, not an untouched scaffold placeholder.
- Model disclosure was repaired: `model_family=gpt` and explicit `model_detail` are present.
- Changelog formatting issue identified by validator audit was repaired.
- Research addendum source-ID duplication feedback was repaired by reusing canonical IDs (`CASE-VECTOR`, `CASE-TURING`, `CASE-AISG-100E`, `CASE-PUNGGOL`, etc.).
- Three key-area features were repaired to include `official_area_sqm` while retaining `announced_area_sqm` and explicit provisional-boundary semantics.
- GeoJSON was reformatted with stable indentation/newlines for reviewability.
- `manifest.json` and `self_check.json` now exist, but intentionally remain diagnostic/scaffold placeholders and must not be presented as passing evidence.
- PR #2 scope cleanup previously confirmed that its diff was limited to this participant package.

## Current known state before finalization

### manifest.json

- `package_state = scaffold`
- SHA-256 entries are placeholder zero hashes.
- `validation_claim.self_checked = false`
- This is not merge-ready evidence.

### self_check.json

- `ok = false`
- `can_enter_formal_review = false`
- four gates are `unknown`
- this is a diagnostic placeholder, not the machine-generated passing report.

## Canonical finalization sequence

Run these from a current checkout synchronized with the latest upstream validator tooling:

```bash
python3 -m pip install -r requirements-review.txt
python3 scripts/finalize_submission.py submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure
python3 scripts/self_check_submission.py submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure --pr-author miyuuteshima984 --mark-self-checked --json
python3 scripts/participant_preflight.py submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure --pr-author miyuuteshima984 --check-push --json
```

Expected behavior:

1. `finalize_submission.py` checks that readable outputs, all five figures, design geometry and required drawings are materially replaced; checks bilingual counterparts; changes `package_state` to `ready_for_review`; refreshes manifest SHA-256 values from actual bytes.
2. `self_check_submission.py --mark-self-checked` runs four gates: deterministic validation, spatial review, visual packaging and professional evidence. Only when all pass does it persist the machine report to `self_check.json`, refresh that file's manifest hash, set `validation_claim.self_checked=true`, and re-run strict validation. If strict verification fails it reverts the persisted evidence.
3. `participant_preflight.py` checks participant path ownership, branch/base availability, PR scope, file-size limits, self-check status and optional push dry-run.

## Important upstream drift observation

At the recovery audit:

- formal working branch head observed: `b9c6c65aa2867c5aba82f83612465da929bb7a78`
- same-fork diagnostic PR #2 head observed: `fb50122d600aa1b8e1166ad883bf8ebc0632ac43`
- current upstream `main` observed later: `960a529e6087176536b2a006e891047ca4377aaa`

`finalize_submission.py` and `self_check_submission.py` were unchanged across the compared upstream points, but `validate_local_submission.py` had changed. Therefore the final four-gate result must be produced with the current upstream tooling, not treated as valid merely because an older checkout passed.

Always re-check these SHAs; they are observations, not permanent constants.

## True blockers (as of this handoff)

- [ ] Formal working branch must be synchronized/rebased/merged with the current upstream `main` before the authoritative final validation.
- [ ] Official `finalize_submission.py` has not yet produced the final `ready_for_review` manifest with real SHA-256 hashes.
- [ ] Official machine-generated four-gate `self_check.json` has not yet been persisted with `--mark-self-checked`.
- [ ] All four gates must actually return PASS using the current upstream trusted validator version.
- [ ] `participant_preflight.py` must pass after finalization/self-check, including scope and push checks.
- [ ] Only after the above should an official upstream PR to `open-city-ai/haidian` be created/declared ready.

## Review feedback that is not currently a validator blocker

- HTML being minified/single-line is reviewability feedback unless a current validator explicitly reports it as an error.
- Chinese PDF non-embedded CID CJK font was recorded as a packaging-quality warning; no current evidence says it is a deterministic blocker.
- Provisional organizer-supplied boundary precision is a disclosed data limitation; current guide/tooling explicitly says organizer geometry gaps themselves should not disqualify an otherwise valid participant package.

## Fixed review feedback — do not reopen unless current validator disproves it

- [x] Canonical source IDs in `research/source-addendum-v0.4.json`
- [x] `official_area_sqm` on all three key areas with provisional semantics preserved
- [x] GeoJSON pretty-print/reviewability cleanup
- [x] Agent model-family/model-detail disclosure
- [x] Changelog format repair
- [x] Presence of diagnostic `manifest.json`
- [x] Presence of diagnostic `self_check.json`

## Do not do

- Do not manually invent SHA-256 values because a connector truncated binary/base64 output.
- Do not mark `self_checked=true` manually.
- Do not overwrite `self_check.json` with redirected stdout and call it canonical evidence; use `--mark-self-checked`.
- Do not open the official upstream PR until current-upstream finalization, four-gate self-check and participant preflight are complete.
- Do not mix unrelated participant paths into the branch.

## Runtime note from the continuation session

The ChatGPT execution container used during this handoff could not resolve `github.com`, so it could not clone the repository locally to execute the Python validators. GitHub repository inspection and this handoff commit were performed through the connected GitHub app. This is an execution-environment limitation, not a repository validation result.

## Next action

Obtain an executable checkout with current upstream `main`, run the canonical sequence above, capture the exact JSON/output, then update this file with:

- current upstream SHA
- final working branch SHA
- finalize result
- four individual gate results and issue IDs/messages
- preflight result
- any repair commits
- final official upstream PR number/status
