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
- 📚 a **machine-readable rules dataset** (`data/*.json`, 30 cited rules) that is itself a citable research artifact.

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

- **Web app (doctors):** open `docs/index.html` in any browser, or visit **`https://hezarani.github.io/dentrx/`**. No install; works offline.
- **Python (researchers):**

  ```bash
  pip install dentrx        # or `pip install -e .` from the repo
  dentrx recommend --pillar prophylaxis_ie --jurisdiction US --cardiac-highest-risk --allergy severe
  ```

  ```python
  import dentrx
  dentrx.recommend("therapeutic_infection", "UK", "adult", {"systemic_involvement": True, "penicillin_allergy": "none"})
  ```

- **Deploy it yourself:** step-by-step in **[`docs/DEPLOY.md`](docs/DEPLOY.md)** (GitHub Pages + PyPI + Zenodo DOI).

## Status

**v0.1 — feature-complete, pending clinical sign-off.** Built: the rule **schema**, cited **source registry** (14 sources), **30 rules** across all four pillars (US + UK, adults + children), the **recommendation engine** (Python + in-browser) with penicillin-allergy branching, the **web app**, a **22-test** guideline-anchored suite (all passing), and the full **evidence dossier**. All 30 rules were verified against the sources cited at release; the UK infective-endocarditis rule is under review against SDCEP's 2nd edition (March 2026) implementation advice. Doses must still be checked against the current primary source before clinical use (guidelines are living documents).

## Repository layout

```
dentrx/
├── data/                 # canonical cited rules datasets — the citable artifact
│   ├── sources.json      # 14 authoritative sources + DOIs/URLs
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
├── tests/test_core.py    # 22 guideline-anchored tests
├── assets/               # banner + social preview
├── paper.md / paper.bib  # JOSS-style preprint stub
├── CITATION.cff · .zenodo.json · LICENSE (MIT) · pyproject.toml
```

## References & prior work

DentRx encodes facts (drug, dose, route, duration) from the sources below and links them; it does not reproduce their text. The machine-readable registry is `data/sources.json`; the figure-level mapping is in [`docs/EVIDENCE.md`](docs/EVIDENCE.md).

**Standards and guidance — United States**

- Carrasco-Labra, A. et al. (2024). Evidence-based clinical practice guideline for the pharmacologic management of acute dental pain in adolescents, adults, and older adults. *Journal of the American Dental Association* 155(2):102–117.e9. [doi:10.1016/j.adaj.2023.10.009](https://doi.org/10.1016/j.adaj.2023.10.009)
- Carrasco-Labra, A. et al. (2023). Evidence-based clinical practice guideline for the pharmacologic management of acute dental pain in children. *Journal of the American Dental Association* 154(9):814–825.e2. [doi:10.1016/j.adaj.2023.06.014](https://doi.org/10.1016/j.adaj.2023.06.014)
- Green, V.G. et al. (2025). Evidence-based clinical practice guidelines for the management of acute dental pain. *American Journal of Emergency Medicine* 89:247–253. [doi:10.1016/j.ajem.2024.12.054](https://doi.org/10.1016/j.ajem.2024.12.054)
- Lockhart, P.B. et al. (2019). Evidence-based clinical practice guideline on antibiotic use for the urgent management of pulpal- and periapical-related dental pain and intraoral swelling. *Journal of the American Dental Association* 150(11):906–921.e12. [doi:10.1016/j.adaj.2019.08.020](https://doi.org/10.1016/j.adaj.2019.08.020)
- Wilson, W.R. et al. (2021). Prevention of viridans group streptococcal infective endocarditis: a scientific statement from the American Heart Association. *Circulation* 143(20):e963–e978. [doi:10.1161/CIR.0000000000000969](https://doi.org/10.1161/CIR.0000000000000969) — correction: *Circulation* 144(9):e192, [doi:10.1161/CIR.0000000000001012](https://doi.org/10.1161/CIR.0000000000001012)
- Sollecito, T.P. et al. (2015). The use of prophylactic antibiotics prior to dental procedures in patients with prosthetic joints. *Journal of the American Dental Association* 146(1):11–16.e8. [doi:10.1016/j.adaj.2014.11.012](https://doi.org/10.1016/j.adaj.2014.11.012)
- American Academy of Orthopaedic Surgeons & American Association of Hip and Knee Surgeons (2024). *The Prevention of Total Hip and Knee Arthroplasty Periprosthetic Joint Infection in Patients Undergoing Dental Procedures: Evidence-Based Clinical Practice Guideline* (adopted 18 November 2024). <https://www.aaos.org/dentalppxcpg>
- U.S. Food and Drug Administration (2017). *FDA Drug Safety Communication: FDA restricts use of prescription codeine pain and cough medicines and tramadol pain medicines in children; recommends against use in breastfeeding women* (20 April 2017). Listed at <https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/codeine-information>
- American Academy of Pediatric Dentistry (2024). Useful medications for oral conditions. In *The Reference Manual of Pediatric Dentistry*. Chicago: AAPD. <https://www.aapd.org/globalassets/media/policies_guidelines/r_usefulmeds.pdf>

**Standards and guidance — United Kingdom**

- Scottish Dental Clinical Effectiveness Programme (2026). *Drug Prescribing for Dentistry: Dental Clinical Guidance* (living web edition; Bacterial Infections section updated May 2026). <https://www.sdcepdentalprescribing.nhs.scot/>
- Scottish Dental Clinical Effectiveness Programme (2026). *Antibiotic Prophylaxis Against Infective Endocarditis: Implementation Advice* (2nd ed., March 2026). <https://www.antibioticprophylaxis.sdcep.org.uk/>
- National Institute for Health and Care Excellence (2008, updated 2016). *Prophylaxis against infective endocarditis: antimicrobial prophylaxis against infective endocarditis in adults and children undergoing interventional procedures* (Clinical guideline CG64). <https://www.nice.org.uk/guidance/cg64>
- Joint Formulary Committee. *British National Formulary* (BNF 91) and *BNF for Children* (2025–26). <https://bnf.nice.org.uk/>

**Evidence that motivated it**

- Portman, D.B., Doyon, J.B. & Buehrle, D.J. (2025). Appropriateness of antibiotic prescriptions written for dental prophylaxis within a regional Veterans Affairs healthcare system based on American Dental Association and American Academy of Orthopaedic Surgeons guidance. *Open Forum Infectious Diseases* 12(8):ofaf432. [doi:10.1093/ofid/ofaf432](https://doi.org/10.1093/ofid/ofaf432)

## License & citation

MIT © 2026 Hossein Boustani Hezarani (DDS). If you use DentRx, please cite it (see [`CITATION.cff`](CITATION.cff)) **and** the underlying guideline you rely on. Guideline sources located via PubMed; see `data/sources.json`.
