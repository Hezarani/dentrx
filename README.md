<div align="center">

![DentRx — dental prescribing, with the guideline attached](assets/banner.png)

# 🦷 DentRx

### An open, guideline-cited dental prescribing reference — antibiotics & analgesics

*NSAID-first analgesia · antibiotic prophylaxis · therapeutic infection · stewardship-forward*
*US (ADA / AHA / AAOS) + UK (SDCEP / NICE / BNF) · adults + children · every recommendation carries its citation*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21874495.svg)](https://doi.org/10.5281/zenodo.21874495)
[![PyPI](https://img.shields.io/pypi/v/dentrx.svg)](https://pypi.org/project/dentrx/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[▶ Open the live web app](https://hezarani.github.io/dentrx/)** · **[pip install dentrx](https://pypi.org/project/dentrx/)**

</div>

> [!WARNING]
> **DentRx is an educational clinical reference, not a prescription.** It does not replace professional judgement. Every dose must be verified against the current primary source and local formulary before clinical use. Guidelines change and differ by country — DentRx tags every rule by jurisdiction and edition, but the prescriber is responsible for the final decision.

---

## What it is

Dental antibiotic and analgesic prescribing is frequently **guideline-discordant** — one 2025 analysis found **67% of dental-prophylaxis prescriptions were not indicated and 72% were inappropriate** — yet the rules live scattered across PDFs and closed apps. DentRx encodes the published rules **once, correctly**, as a tested, versioned, **cited** dataset, and turns them into:

- 🩺 a **zero-install web app** a clinician just opens in a browser (nothing to install; works offline after first load) — ✅ built (`docs/`);
- 🐍 a **Python package** (`dentrx`) that returns a structured recommendation + the citation + a reasoning trace — ✅ built;
- 📚 a **machine-readable rules dataset** (`data/*.json`, 27 cited rules) that is itself a citable research artifact.

Call shape:

```python
dentrx.recommend(scenario="acute_dental_pain", jurisdiction="US", population="adult")
# -> first-line: NSAID ± acetaminophen; ibuprofen 400 mg q4–6h (max 2400 mg/day) ...
#    + source: ADA 2024 (doi:10.1016/j.adaj.2023.10.009) + disclaimer + reasoning trace
```

## The four pillars

| Pillar | The rule in one line | Governing sources |
|---|---|---|
| **Analgesia** | Treat pain with NSAID ± acetaminophen, not antibiotics; opioids reserved | ADA 2024/2023, FDA, AAPD · SDCEP/BNF |
| **IE prophylaxis** | Only highest-risk cardiac patients; amoxicillin 2 g; no clindamycin | AHA 2021 · SDCEP/NICE |
| **Prosthetic-joint prophylaxis** | Not routinely recommended (reinforced by AAOS 2024) | ADA 2015 + AAOS 2024 · SDCEP |
| **Therapeutic infection** | Definitive dental treatment first; antibiotics only with systemic involvement | ADA 2019 · SDCEP/NICE |

Full, cited detail with exact figures: **[`docs/EVIDENCE.md`](docs/EVIDENCE.md)**.

## Design principles

1. **Facts + citation, never copied prose.** Doses are facts; guideline text is copyrighted. DentRx paraphrases and links the DOI, and never republishes ADA CDT codes.
2. **Never auto-prescribe.** Output is a reference with a reasoning trace and a clear disclaimer; a clinician decides.
3. **Penicillin-allergy branching is built in** (none / non-severe / severe).
4. **Every rule is versioned, dated, and jurisdiction-tagged** — because guidelines are living and differ by country.
5. **Stewardship-forward:** where the evidence says *don't* prescribe, that shows up as loudly as any drug.

## Try it

- **Web app (doctors):** open `docs/index.html` in any browser, or once deployed, visit **`https://hezarani.github.io/dentrx/`**. No install; works offline.
- **Python (researchers):**

  ```bash
  pip install dentrx        # after PyPI release; or `pip install -e .` from the repo
  dentrx recommend --pillar prophylaxis_ie --jurisdiction US --cardiac-highest-risk --allergy severe
  ```

  ```python
  import dentrx
  dentrx.recommend("therapeutic_infection", "UK", "adult", {"systemic_involvement": True, "penicillin_allergy": "none"})
  ```

- **Deploy it yourself:** step-by-step in **[`docs/DEPLOY.md`](docs/DEPLOY.md)** (GitHub Pages + PyPI + Zenodo DOI).

## Status

**v0.1 — feature-complete, pending clinical sign-off.** Built: the rule **schema**, cited **source registry** (12 sources), **27 rules** across all four pillars (US + UK, adults + children), the **recommendation engine** (Python + in-browser) with penicillin-allergy branching, the **web app**, a **16-test** guideline-anchored suite (all passing), and the full **evidence dossier**. 25/27 rules are figure-verified; 2 cells (UK IE, UK paediatric therapeutic) are flagged *to-verify*. **A DDS reviews `docs/EVIDENCE.md` and signs off before the first tagged release.**

## Repository layout

```
dentrx/
├── data/                 # canonical cited rules datasets — the citable artifact
│   ├── sources.json      # 12 authoritative sources + DOIs/URLs
│   ├── analgesics.json
│   ├── prophylaxis_ie.json
│   ├── prophylaxis_joint.json
│   └── therapeutic_infection.json
├── schema/rule.schema.json   # JSON Schema for the datasets
├── dentrx/               # Python package (engine + CLI)
│   ├── core.py           # recommend() + allergy branching
│   └── cli.py
├── docs/                 # GitHub Pages site
│   ├── index.html        # the zero-install web app (Apple-style UI)
│   ├── data.js           # auto-bundled datasets (offline)
│   ├── EVIDENCE.md       # full cited clinical foundation
│   └── DEPLOY.md         # step-by-step deployment guide
├── scripts/build_web_data.py  # bundles data/ -> docs/data.js
├── tests/test_core.py    # 16 guideline-anchored tests
├── assets/               # banner + social preview
├── paper.md / paper.bib  # JOSS-style preprint stub
├── CITATION.cff · .zenodo.json · LICENSE (MIT) · pyproject.toml
```

## License & citation

MIT © 2026 Hossein Boustani Hezarani (DDS). If you use DentRx, please cite it (see [`CITATION.cff`](CITATION.cff)) **and** the underlying guideline you rely on. Guideline sources located via PubMed; see `data/sources.json`.
