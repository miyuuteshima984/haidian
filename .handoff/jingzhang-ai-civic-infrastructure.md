# 京张城市完整度 / JING-ZHANG CITY COMPLETENESS — Continuation Handoff

> Future continuation: read this file first. This handoff deliberately lives on a separate branch and outside the formal submission package because the deterministic validator rejects arbitrary `research/*` files inside a proposal directory.

## Targets

- Fork: `miyuuteshima984/haidian`
- Formal branch: `submission/miyuuteshima984/jingzhang-ai-civic-infrastructure`
- Formal package: `submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure/`
- Handoff branch: `handoff/jingzhang-ai-civic-infrastructure`
- Handoff file: `.handoff/jingzhang-ai-civic-infrastructure.md`
- Current-base diagnostic PR: `miyuuteshima984/haidian#3`
- Official target only after all checks pass: `open-city-ai/haidian:main`

## Recovered old-conversation checkpoint

The old conversation stopped at internal step **7e-4a**, which proposed manually retrieving seven PNG binaries and calculating SHA-256 because connector base64 output was truncated. That workaround is retired. The canonical finalizer reads full local bytes and calculates SHA-256 itself. Never invent final hashes manually.

## Confirmed fixed before canonical run

- bilingual v2 formal proposal and 13 required sections
- five bilingual core figure pairs
- bilingual report HTML, visual pages, A3/A0 PDFs
- nine required GeoJSON layers
- model disclosure (`model_family=gpt`, explicit `model_detail`)
- changelog-format issue
- canonical source IDs in earlier research addendum work
- `official_area_sqm` on all three provisional key areas
- strict manifest schema migrated to `0.2.0`
- formal branch rebuilt cleanly on current upstream without unrelated participant paths
- projected land-use seam overlaps fixed by densifying `LU-013` edge breakpoints; all six >1 m² overlaps went to zero

## First authoritative canonical GitHub runner result

Temporary GitHub runner executed the repository's actual scripts on the formal branch.

Result:

- `finalize_submission.py`: **PASS** (`rc=0`)
- `self_check_submission.py --mark-self-checked --json`: **FAIL** (`rc=1`)
- `participant_preflight.py`: not run because self-check correctly failed

### Gate results

- deterministic validation: **FAIL — exactly one error**
- spatial review: **PASS**
- visual review: **PASS**
- professional evidence review: **PASS**
- review dependencies: none missing

### Only deterministic blocker

`submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure/research/CONTINUATION.md` is not an allowed submission-package path.

The validator permits the prescribed proposal/changelog/root package files plus allowed `assets/*`, `geometry/*`, `drawings/*`, `report/*`, localized visual files and `visual/assets/*`; arbitrary `research/*` is rejected.

Therefore this handoff has been moved to this dedicated branch. The next formal-branch repair is to delete `research/CONTINUATION.md` and rerun the canonical workflow.

### Spatial PASS details

Only three `KEY_AREA_PROVISIONAL` minor findings remain, one per provisional key area. The machine message explicitly says content scoring remains eligible.

Computed metrics:

- `site_area_sqm = 11412825.386`
- `green_space_area_sqm = 2225592.728`
- `public_space_area_sqm = 386029.358`
- `building_footprint_area_sqm = 1024945.371`
- `green_ratio = 0.195008`
- `public_space_ratio = 0.033824`

### Visual PASS details

- `issues: []`
- HTML required metrics matched exactly.

### Professional PASS details

- `issues: []`
- standard matrix items: 6
- design depth items: 15
- known metric references required: 32
- proposal format version: 2
- reference counts: source 19 / standard 6 / depth 15 / data 11 / metric 32

## Pending-self-check warnings are not independent blockers

After finalization, deterministic validation warned that `ready_for_review` packages still needed:

- `validation_claim.self_checked=true`
- persisted `self_check.ok=true`
- `can_enter_formal_review=true`
- persisted pass/blocking four-gate records

Those are expected temporary warnings during `--mark-self-checked`; they should disappear once the one real deterministic error is removed and the persistence step succeeds.

The provisional site-boundary warning is advisory and explicitly non-disqualifying.

## Canonical sequence

```bash
python3 scripts/finalize_submission.py submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure
python3 scripts/self_check_submission.py submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure --pr-author miyuuteshima984 --mark-self-checked --json
python3 scripts/participant_preflight.py submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure --pr-author miyuuteshima984 --check-push --json
```

The temporary automation branch runs this on GitHub-hosted Ubuntu with current repository dependencies because the ChatGPT container cannot resolve GitHub DNS.

## TODO

- [ ] Remove illegal `research/CONTINUATION.md` from formal package (handoff is preserved here instead).
- [ ] Mirror that clean formal head to diagnostic PR #3.
- [ ] Trigger temporary canonical runner again.
- [ ] Expect all four self-check gates to pass; inspect exact machine output rather than assuming.
- [ ] If self-check passes, runner should persist machine `self_check.json` and real manifest SHA-256 values.
- [ ] Run/confirm `participant_preflight.py --check-push --json` PASS.
- [ ] Re-check current upstream immediately before official PR because upstream moves rapidly.
- [ ] If current validator tooling/base changed, rebuild/revalidate without touching package semantics unnecessarily.
- [ ] Only after all of the above create the official upstream PR.

## Non-blocking review feedback

- single-line/minified HTML is reviewability feedback unless a current validator says otherwise
- several GeoJSON files are still minified; do not falsely claim all pretty-print feedback was fixed
- non-embedded CID CJK PDF font was a packaging-quality warning, not a validator blocker
- provisional organizer geometry remains a disclosed data limitation and is explicitly eligible for content scoring

## Do not do

- do not place this handoff MD back inside the formal proposal directory
- do not invent SHA-256 values
- do not manually set `self_checked=true`
- do not call static checks a machine PASS
- do not open the official upstream PR before finalization + persisted self-check + preflight all pass
