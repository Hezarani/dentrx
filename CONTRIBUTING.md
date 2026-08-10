# Contributing to DentRx

Thanks for helping improve DentRx. Because this is a **clinical reference**, correctness and traceability matter more than anything else.

## Ground rules

1. **Every rule cites a source.** Add or update the source in `data/sources.json` (with a DOI or official URL) and reference its key from the rule.
2. **Encode facts, not prose.** Store drug/dose/route/frequency/duration — never copy copyrighted guideline text, and never add ADA CDT procedure codes.
3. **Mark verification honestly.** Set `"status": "verified"` only when the figures have been checked against the primary source this cycle. Otherwise use `"pending_verification"`.
4. **A clinician signs off.** Clinical changes should be reviewed by a qualified dentist before release.

## Workflow

```bash
# 1. edit the relevant data/*.json
# 2. rebuild the browser bundle + revalidate
python scripts/build_web_data.py
python -m pytest -q
# 3. open docs/index.html to eyeball the change
```

- Add a test in `tests/test_core.py` for any new clinical behaviour (especially allergy branches and "do-not-prescribe" logic).
- Keep the schema (`schema/rule.schema.json`) authoritative; new fields go there first.
- Update `docs/EVIDENCE.md` so the dossier stays the single source of truth.

## Reporting problems

Open an issue describing the scenario, the expected guideline-based answer, and the source. Clinical-accuracy issues are top priority.
