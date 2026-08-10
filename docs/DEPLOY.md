# DentRx — Deployment & Setup Guide

A copy-paste, step-by-step guide to publish DentRx so doctors can use it and researchers can cite it. Nothing here needs coding experience — just follow the steps in order.

There are three things you can publish (do **A** first; **B** and **C** are optional and can wait):

- **A. The web app** → a public link doctors open in any browser (via GitHub + GitHub Pages). *~15 min.*
- **B. The Python package** → `pip install dentrx` for researchers (via PyPI). *~15 min.*
- **C. A citable DOI** → a permanent DOI + "cite this" (via Zenodo). *~10 min.*

---

## Before you start — what you need

| Tool / account | For | Link |
|---|---|---|
| A **GitHub** account | Hosting the code + the free web app | https://github.com/join |
| **git** installed on your Mac/PC | Uploading the folder | https://git-scm.com/downloads |
| (Optional) **Python 3.9+** | Building the Python package | https://www.python.org/downloads/ |
| (Optional) A **PyPI** account | `pip install dentrx` | https://pypi.org/account/register/ |
| (Optional) A **Zenodo** account | The citable DOI | https://zenodo.org/signup/ |

> Tip: sign in to Zenodo **with your GitHub account** — it makes Part C one click.

---

## Part A — Put the web app online (GitHub Pages)

The app is 100% static (just `docs/index.html` + `docs/data.js`), so GitHub Pages hosts it for free.

### A1. Create the repository on GitHub
1. Go to https://github.com/new
2. **Repository name:** `dentrx`
3. Visibility: **Public**. Do **not** add a README/license (we already have them).
4. Click **Create repository**. Leave the page open — you'll need the URL it shows.

### A2. Upload the folder from your computer
Open a terminal, then run these (replace `Hezarani` if your username differs):

```bash
cd "/home/axiom/Desktop/Claude-Cowork/Projects/DentGit/dentrx"   # the DentRx folder
git init
git add .
git commit -m "DentRx v0.1: guideline-cited dental prescribing reference"
git branch -M main
git remote add origin https://github.com/Hezarani/dentrx.git
git push -u origin main
```

> If `git` asks you to log in, use your GitHub username and a **Personal Access Token** as the password (GitHub → Settings → Developer settings → Tokens → *Generate new token (classic)* → tick `repo`). Your DentGit credentials note has details.

### A3. Turn on GitHub Pages
1. In your repo: **Settings → Pages**.
2. **Source:** *Deploy from a branch*.
3. **Branch:** `main`, **Folder:** `/docs`. Click **Save**.
4. Wait ~1 minute, then refresh. Pages shows your live URL:

   **`https://Hezarani.github.io/dentrx/`**

That link is the doctor-facing app. Share it anywhere. It works on phones, works offline after first load, and needs no install.

### A4. Make the repo look great (2 minutes, drives trust + stars)
- Repo home → ⚙️ (top right) → **Website:** paste your Pages URL.
- **Topics:** add `dentistry`, `prescribing`, `antibiotic-stewardship`, `clinical-decision-support`, `evidence-based-dentistry`, `open-science`.
- **Settings → General → Social preview:** upload `assets/social-preview.png` (already in the repo) so links unfurl with a banner.

---

## Part B — Publish the Python package to PyPI (optional)

For the research/citation side (`pip install dentrx`).

```bash
cd "/home/axiom/Desktop/Claude-Cowork/Projects/DentGit/dentrx"
python -m pip install --upgrade build twine
python scripts/build_web_data.py     # sync data into the package first
python -m build                      # creates dist/*.whl and dist/*.tar.gz
python -m twine upload dist/*         # log in with your PyPI token
```

Then anyone can:

```bash
pip install dentrx
dentrx recommend --pillar prophylaxis_ie --jurisdiction US --cardiac-highest-risk --allergy severe
```

> **Version note (important):** a version number on PyPI is permanent. Ship as `0.1.0`; any fix needs a bump to `0.1.1` in `pyproject.toml`, `CITATION.cff`, and `dentrx/core.py`. (Same lesson as ToothNotation.)

---

## Part C — Get a citable DOI (Zenodo) (optional)

1. Go to https://zenodo.org , log in **with GitHub**.
2. Left menu → **GitHub**. Find `dentrx` in the list and flip the switch **On**.
3. Back on GitHub: **Releases → Create a new release**.
   - **Tag:** `v0.1.0`  · **Title:** `DentRx v0.1.0`  · add a short description → **Publish release**.
4. Zenodo automatically archives it and mints a **DOI**. Copy the DOI badge from Zenodo.
5. Paste the badge at the top of `README.md`, and add the DOI to `CITATION.cff` and `.zenodo.json`.

Now DentRx is a citable research output — a repo *and* a DOI people can reference in papers.

---

## Updating a rule later (maintenance)

1. Edit the relevant file in `data/` (e.g. `data/therapeutic_infection.json`). Keep the `sources` + `source_locator` accurate and bump `status` to `verified` only after you (the DDS) confirm it.
2. Rebuild the browser bundle and re-run the checks:
   ```bash
   python scripts/build_web_data.py
   python -m pytest -q
   ```
3. Commit & push:
   ```bash
   git add -A && git commit -m "Update <pillar>: <what changed>" && git push
   ```
   Pages redeploys automatically in ~1 minute.

---

## Pre-flight checklist

- [ ] `python -m pytest -q` → all tests pass
- [ ] `python scripts/build_web_data.py` → `docs/data.js` regenerated
- [ ] Opened `docs/index.html` locally; disclaimer gate shows; each pillar returns a cited card
- [ ] All ⏳ *to-verify* cells reviewed by a DDS before you advertise the tool
- [ ] README, LICENSE, CITATION.cff, disclaimers all present
- [ ] (A) Pages live · (B) PyPI uploaded · (C) Zenodo DOI minted & badge added

_Questions this guide doesn't cover? The repo's `README.md` and `docs/EVIDENCE.md` have the rest._
