# Changelog

All notable changes to DentRx are documented here. Format based on Keep a Changelog; versioning is semantic.

## [0.1.0] — 2026-08-09

### Added
- Initial release. Four clinical pillars — acute-pain analgesia, infective-endocarditis prophylaxis, prosthetic-joint prophylaxis, and therapeutic antibiotics for pulpal/periapical infection.
- **27 guideline-cited rules** across US (ADA/AHA/AAOS/FDA/AAPD) and UK (SDCEP/NICE/BNF/BNFc), for adults and children.
- Versioned JSON rules dataset with a JSON Schema, and a source registry of 14 authoritative sources with DOIs/URLs.
- Recommendation engine (Python `dentrx` package + CLI, and an in-browser port) with penicillin-allergy branching (none / non-severe / severe).
- Zero-install, offline-capable web app (`docs/index.html`) with an accessible, Apple-style UI, a mandatory disclaimer gate, print/export, and SEO metadata.
- Evidence dossier (`docs/EVIDENCE.md`), deployment guide (`docs/DEPLOY.md`), JOSS-style preprint stub, `CITATION.cff`, and Zenodo metadata.
- 16 guideline-anchored tests.

### Notes
- Educational reference only — not a prescription. Clinical sign-off by a DDS precedes clinical reliance.
