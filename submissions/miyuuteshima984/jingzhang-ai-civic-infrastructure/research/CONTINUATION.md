# 京张城市完整度 / JING-ZHANG CITY COMPLETENESS — Continuation Handoff

> Persistent handoff for future ChatGPT/project conversations. Read this file first and continue from the first unchecked item; do not restart the audit from scratch.

## Working target

- Fork: `miyuuteshima984/haidian`
- Formal branch: `submission/miyuuteshima984/jingzhang-ai-civic-infrastructure`
- Package: `submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure/`
- Same-fork diagnostic PR: `miyuuteshima984/haidian#2`
- Diagnostic branch: `validation/miyuuteshima984/jingzhang-ai-civic-infrastructure`
- Official target, only after preflight: `open-city-ai/haidian:main`
- PR #2 is a trusted-validation staging PR, **not** the official upstream submission PR.

## Recovered old-conversation checkpoint

The old long conversation stopped at internal step **7e-4a**, which proposed manually retrieving seven PNG binaries and calculating SHA-256 because connector base64 output was truncated. That workaround is retired. `scripts/finalize_submission.py` reads full local bytes and calculates SHA-256 itself. Do not guess or manually paste final hashes.

## Current upstream / branch topology

As of this handoff update:

- upstream `open-city-ai/haidian:main`: `6d4f56abadb2dda1c8b0e21fbd9fc31f18b8b8e4`
- this upstream commit adds `scripts/refresh_submission_manifest.py`; it does not replace finalization/self-check and did not change the validator semantics relevant to the fixes below.
- package subtree carried forward: `2052b074f497b9b3a43715194c227f97d57c16c9`
- a clean one-parent submission commit was rebuilt directly on current upstream. Before moving refs, GitHub compare confirmed `ahead=1`, `behind=0`, and every changed file remained under this participant package.
- fork `main` was fast-forwarded to the same upstream SHA so same-fork preflight/base comparisons use a current base.

Always re-check upstream before the final official PR because this repository moves rapidly.

## Confirmed completed work

- [x] Chinese-primary bilingual formal proposal exists.
- [x] Chinese/English proposals use the 13 mandatory formal-section sequence.
- [x] `proposal_format_version: "2"` and `bilingual_contract_version: "1"` are present.
- [x] Chinese primary points to `proposal.en.md`; English counterpart points back with `translation_of: proposal.md`.
- [x] Five bilingual core figure pairs exist.
- [x] Bilingual report HTML, offline visual pages, A3 booklet and A0 boards exist.
- [x] Nine required GeoJSON layers exist.
- [x] `constraints.geojson` is intentionally empty with an explicit official-data-gap disclosure.
- [x] Model disclosure repaired: `model_family=gpt` plus explicit `model_detail`.
- [x] Changelog-format validator issue repaired.
- [x] Research addendum canonical source-ID duplication feedback repaired in the earlier diagnostic work.
- [x] Three key-area features contain `official_area_sqm` while preserving provisional-boundary semantics.
- [x] Diagnostic `manifest.json` exists.
- [x] Diagnostic `self_check.json` exists.
- [x] PR scope was cleaned and is limited to this participant package.
- [x] Formal branch was rebuilt as a clean one-parent commit on current upstream instead of carrying hundreds of unrelated merge commits.

## True blocker found and fixed: strict manifest schema

Current upstream introduced the strict manifest migration contract. Newly added/copied/renamed manifests must use schema `0.2.x`; our newly added manifest was still `0.1.0`.

Fix already applied before the latest clean rebase:

- commit at the time: `7e7ad918b644698fa470bc7dff21073fb3c7afb7`
- change: `manifest.schema_version` → `0.2.0`

The manifest intentionally remains `package_state=scaffold`, zero-hashed and `self_checked=false` until the canonical finalizer runs. Schema migration is fixed; readiness is not yet claimed.

## True blocker found and fixed: projected land-use seam overlaps

Using the current `spatial_review.py` projection/threshold logic (EPSG:4548), six `LU-013` public-green-spine seams overlapped adjacent right-side land-use polygons by more than the 1 m² major-issue threshold:

- LU-002 / LU-013: ~9.48 m²
- LU-004 / LU-013: ~10.58 m²
- LU-006 / LU-013: ~10.43 m²
- LU-008 / LU-013: ~10.98 m²
- LU-010 / LU-013: ~15.09 m²
- LU-012 / LU-013: ~25.61 m²

Cause: LU-013 used one long WGS84 vertical chord while neighboring polygons used segmented edges; after projection the chords were not identical.

Fix already applied before the latest clean rebase:

- commit at the time: `3080218f4c479bf45d5f13f17865840df1c39b3f`
- densified both LU-013 vertical edges at the same latitude breakpoints used by neighbors
- design intent/boundary meaning unchanged
- updated LU-013 declared area and `metrics.json.land_use_park_green_sqm` to `2157782.029`

Local reproduction after the fix:

- all six pairwise overlaps: `0`
- land-use union gap: ~`89.24 m²`, below the current allowed threshold
- outside-site area: `0`
- site / green / public-space / building recomputations remain consistent with current metric tolerances

This is a repaired validator blocker, not formatting feedback.

## Static four-gate audit after repairs

These are static/local reproductions, **not** a persisted machine PASS. Final status must come from the trusted scripts.

### Spatial

No remaining major/blocking issue found after the LU-013 seam repair. Key areas remain intentionally provisional and should produce disclosure/advisory findings rather than eligibility failure.

### Visual

`visual/index.html` contains all current required visible markers:

`总览地图 / 三层范围 / 重点区域 / 用地分区 / 交通慢行 / 蓝绿公共空间 / 建筑 / 更新项目 / AI 场景 / 核心指标 / 任务覆盖 / 自检状态 / 来源 / 假设`

Required HTML metrics match `metrics.json`:

- `site_area_sqm = 11412825.386`
- `green_ratio = 0.195008`
- `public_space_ratio = 0.033824`

No obvious forbidden remote/active-content pattern was found.

### Professional evidence

For proposal format v2, current professional review primarily requires full mandatory-standard coverage and required design-depth coverage. Static inspection found those matrices populated for the current contract; no obvious major/blocking gap remains.

### Deterministic/content

Static inspection found:

- valid participant author/path mapping
- registered tracks/scenarios within current limits
- mandatory v2 formal sections and evidence anchors present
- bilingual front-matter mapping present
- required package files present
- allowed land-use/building enums used in the inspected geometry
- risk/spatial structured evidence populated

Do not convert this static audit into `self_checked=true`; the trusted run still controls the claim.

## Current diagnostic placeholder state

### manifest.json

- `schema_version = 0.2.0` (fixed)
- `package_state = scaffold`
- SHA-256 entries still zero placeholders
- `validation_claim.self_checked = false`

### self_check.json

- `ok = false`
- `can_enter_formal_review = false`
- four gates are diagnostic `unknown`

These states are intentional until canonical finalization.

## Canonical sequence still required

```bash
python3 -m pip install -r requirements-review.txt
python3 scripts/finalize_submission.py submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure
python3 scripts/self_check_submission.py submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure --pr-author miyuuteshima984 --mark-self-checked --json
python3 scripts/participant_preflight.py submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure --pr-author miyuuteshima984 --check-push --json
```

`self_check_submission.py --mark-self-checked` must be allowed to persist the actual machine report and refresh its manifest hash. Do not redirect stdout into `self_check.json` as a substitute.

## Remaining true blockers / TODO

- [x] Cleanly synchronize the package to current upstream without unrelated participant paths.
- [x] Migrate newly added manifest to strict schema `0.2.0`.
- [x] Repair spatial LU-013 projected seam overlaps.
- [ ] Trigger/run the current trusted diagnostic validator and capture its exact blocker list.
- [ ] Run canonical `finalize_submission.py` to produce `ready_for_review` + actual SHA-256 values.
- [ ] Run `self_check_submission.py --mark-self-checked --json`; all four gates must pass and persist the real `self_check.json`.
- [ ] Run `participant_preflight.py --check-push --json` successfully.
- [ ] Re-check upstream main immediately before official submission; refresh/rebase if validator semantics or base have moved.
- [ ] Only then create the official upstream PR.

## Review feedback that is not currently a validator blocker

- Single-line/minified HTML is reviewability feedback unless a current validator reports otherwise.
- Several formal-branch GeoJSON files are still minified; do **not** claim that all GeoJSON pretty-print feedback has been fixed. Formatting can be cleaned later, but it is not currently a known gate blocker.
- Chinese PDF non-embedded CID CJK font was recorded as a packaging-quality warning, not a known deterministic blocker.
- The four PDFs are small (~4.5–7.5 KiB), but current empty-PDF logic does not reject by size alone; keep page/content QA on the checklist.
- Organizer-provided provisional-boundary precision is a disclosed data limitation and is not supposed to disqualify an otherwise valid participant package.

## Fixed review feedback — do not reopen unless current tooling disproves it

- [x] canonical source IDs in the research addendum
- [x] `official_area_sqm` on all three key areas while retaining provisional semantics
- [x] agent model-family/model-detail disclosure
- [x] changelog-format repair
- [x] diagnostic manifest/self-check presence
- [x] strict manifest `0.2.0` migration
- [x] projected land-use seam overlap repair

## Runtime / validation channel note

The ChatGPT execution container cannot resolve GitHub DNS, so normal `git clone` is unavailable. The connected GitHub app can still read/write Git objects. The fork's `main` now contains the current trusted `pull_request_target` workflow, and diagnostic PR #2 is open, non-draft, mergeable, and intentionally exists to obtain trusted validator output without opening the official upstream PR. The next branch update should be used to trigger that diagnostic workflow.

## Do not do

- Do not manually invent final SHA-256 values.
- Do not manually set `self_checked=true`.
- Do not call static audit results a machine PASS.
- Do not create the official upstream PR before finalization, persisted self-check and participant preflight pass.
- Do not mix unrelated participant paths into the submission branch.
