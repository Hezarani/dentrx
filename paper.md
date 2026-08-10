---
title: "DentRx: an open, guideline-cited dental prescribing reference for antibiotics and analgesics"
tags:
  - dentistry
  - prescribing
  - antibiotic stewardship
  - clinical decision support
  - evidence-based dentistry
  - open science
authors:
  - name: Hossein Boustani Hezarani
    orcid: 0009-0007-8481-0498
    affiliation: 1
affiliations:
  - name: Independent researcher (DDS)
    index: 1
date: 9 August 2026
bibliography: paper.bib
---

# Summary

`DentRx` is an open-source, dependency-free reference implementation of published dental
prescribing guidance for **antibiotics and analgesics**. It encodes, as a versioned and
citation-linked dataset, the rules that govern (1) acute-pain analgesia, (2) antibiotic
prophylaxis for infective endocarditis, (3) antibiotic prophylaxis for prosthetic joints,
and (4) therapeutic antibiotics for pulpal/periapical infection. A small engine maps a
clinical scenario plus patient factors (age group, penicillin-allergy status, systemic
involvement, cardiac risk, ability to take oral medication) to the applicable
recommendation, and returns it together with the **source citation, a reasoning trace, and
a mandatory disclaimer**. The same dataset powers a zero-install browser application and a
Python package (`pip install dentrx`), and covers both United States (ADA, AHA, AAOS, FDA,
AAPD) and United Kingdom (SDCEP, NICE/UKHSA, BNF/BNFc) guidance for adults and children.
`DentRx` is an educational reference, not a prescribing authority; it never auto-prescribes.

# Statement of need

Dental antibiotic and analgesic prescribing is frequently discordant with guidelines.
Analyses report that a large majority of dental antibiotic-prophylaxis prescriptions are
not indicated or are otherwise inappropriate [@suda2025appropriateness], and antibiotic
stewardship in dentistry is an active public-health priority. At the same time, the
governing recommendations are current but fragmented and *living*: the ADA acute dental
pain guideline was published in 2024 [@carrascolabra2024adults] (children, 2023
[@carrascolabra2023children]); the ADA guideline on antibiotics for pulpal/periapical
conditions in 2019 [@lockhart2019]; the AHA infective-endocarditis statement in 2021
[@wilson2021]; the prosthetic-joint position in ADA 2015 [@sollecito2015] and, more
recently, the 2024 AAOS clinical practice guideline; and the UK SDCEP *Drug Prescribing for
Dentistry* is maintained as a continuously updated resource. Practitioners typically
re-read these rules from PDFs or closed apps.

Despite this, there is **no open, tested, embeddable library** that encodes the rules with
their citations. Existing tools are closed mobile apps, static association PDFs, or
practice-management systems. `DentRx` fills that gap with a transparent, human-in-the-loop
reference that is (a) directly usable by clinicians as a zero-install web app, and (b)
reusable by researchers and educators as a cited dataset and package.

# Functionality

- **Cited rules dataset.** Each rule stores the drug, dose, route, frequency, and duration
  (facts, not copyrighted prose), plus its indication, patient triggers, jurisdiction,
  guideline strength/certainty, a pointer to the source, and a verification status. A JSON
  Schema validates every dataset file.
- **Engine.** `recommend(pillar, jurisdiction, population, patient)` returns the ranked
  matching rules with resolved citations, the inputs that would sharpen the match, and a
  disclaimer. Penicillin-allergy branching (none / non-severe / severe) is built in, and
  cephalosporins are withheld for severe (anaphylactic) allergy.
- **Interfaces.** A command-line tool, a Python API, and a static, offline-capable web
  application that runs entirely client-side.
- **Safety by design.** Every output carries a disclaimer; the tool surfaces "do not
  prescribe / definitive dental treatment" recommendations as prominently as any drug, in
  line with stewardship guidance; and it never republishes ADA-copyrighted CDT codes.

# Quality control

Recommendations are traceable to a single evidence dossier (`docs/EVIDENCE.md`), which is in
turn traceable to named primary sources with DOIs/URLs (`data/sources.json`). A test suite
asserts guideline-anchored behaviours — for example, that severe penicillin allergy never
yields a cephalosporin, that clindamycin is never offered for endocarditis prophylaxis, and
that pulpal/periapical infection without systemic involvement returns definitive dental
treatment rather than an antibiotic. Cells not yet verified against their primary source are
explicitly flagged, and clinical sign-off by a licensed dentist precedes any release.

# Availability

`DentRx` is distributed under the MIT license. Source, dataset, web app, and documentation
are available on GitHub; the Python package is on PyPI; releases are archived with a DOI.

# References
