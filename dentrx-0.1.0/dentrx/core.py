"""DentRx core engine — dependency-free rule lookup over the cited JSON datasets.

The engine matches a clinical scenario + patient factors to guideline-cited rules and
returns the recommendation together with its source citation, a reasoning trace, and a
mandatory disclaimer. It never decides for the clinician.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from functools import lru_cache

__version__ = "0.1.0"

DISCLAIMER = (
    "DentRx is an educational clinical reference, not a prescription. It does not replace "
    "professional judgement, current official guidelines, or local formularies. Verify every "
    "dose against the primary source before clinical use. Definitive dental treatment is the "
    "priority; antibiotics and analgesics are adjuncts."
)

PILLARS = {
    "analgesia": "Acute-pain analgesia",
    "prophylaxis_ie": "Antibiotic prophylaxis — infective endocarditis",
    "prophylaxis_joint": "Antibiotic prophylaxis — prosthetic joints",
    "therapeutic_infection": "Therapeutic antibiotics — pulpal/periapical infection",
}

TRIGGER_KEYS = (
    "penicillin_allergy",       # "none" | "non_severe" | "severe"
    "systemic_involvement",     # bool
    "cardiac_highest_risk",     # bool
    "prosthetic_joint",         # bool
    "can_take_oral",            # bool
)


def _data_dir() -> Path:
    """Locate the canonical data directory (env override > package copy > repo root)."""
    env = os.environ.get("DENTRX_DATA")
    if env and Path(env).is_dir():
        return Path(env)
    here = Path(__file__).resolve().parent
    for cand in (here / "data", here.parent / "data"):
        if cand.is_dir():
            return cand
    raise FileNotFoundError(
        "DentRx data directory not found. Set DENTRX_DATA or run from the repository."
    )


@lru_cache(maxsize=1)
def load_sources() -> dict:
    return json.loads((_data_dir() / "sources.json").read_text(encoding="utf-8"))["sources"]


@lru_cache(maxsize=1)
def load_rules() -> list:
    """Load every rule across all pillar files, tagging each with its dataset disclaimer."""
    rules = []
    for f in sorted(_data_dir().glob("*.json")):
        if f.name == "sources.json":
            continue
        data = json.loads(f.read_text(encoding="utf-8"))
        disclaimer = data.get("meta", {}).get("disclaimer", "")
        for r in data.get("rules", []):
            r = dict(r)
            r["_dataset_disclaimer"] = disclaimer
            rules.append(r)
    return rules


def pillars() -> dict:
    """Return the available pillars {key: human label}."""
    return dict(PILLARS)


def _pop_match(rule_group: str, population: str) -> bool:
    if rule_group == "all":
        return True
    if rule_group == "adult":
        return population in ("adult", "adolescent")
    if rule_group == "adolescent":
        return population == "adolescent"
    if rule_group == "child":
        return population == "child"
    return rule_group == population


def _evaluate(triggers: dict, patient: dict):
    """Return (compatible, matched_count, missing_keys) for a rule's triggers vs patient."""
    matched, missing, compatible = 0, [], True
    for key, want in triggers.items():
        if key not in patient or patient[key] is None:
            missing.append(key)
            continue
        pv = patient[key]
        ok = (pv in want) if isinstance(want, list) else (pv == want)
        if ok:
            matched += 1
        else:
            compatible = False
    return compatible, matched, missing


def _resolve_sources(keys, sources):
    out = []
    for k in keys:
        s = sources.get(k)
        if not s:
            continue
        out.append({
            "key": k,
            "organization": s.get("organization"),
            "title": s.get("title"),
            "citation": s.get("citation"),
            "year": s.get("year"),
            "doi": s.get("doi"),
            "url": s.get("url") or (f"https://doi.org/{s['doi']}" if s.get("doi") else None),
        })
    return out


def _format(rule: dict, sources: dict) -> dict:
    return {
        "id": rule["id"],
        "pillar": rule["pillar"],
        "jurisdiction": rule["jurisdiction"],
        "population": rule.get("population", {}),
        "scenario": rule.get("scenario", {}),
        "recommendation": rule.get("recommendation", {}),
        "contraindications": rule.get("contraindications", []),
        "cautions": rule.get("cautions", []),
        "rationale": rule.get("rationale", ""),
        "strength": rule.get("strength"),
        "certainty": rule.get("certainty"),
        "status": rule.get("status"),
        "source_locator": rule.get("source_locator"),
        "citations": _resolve_sources(rule.get("sources", []), sources),
        "disclaimer": rule.get("_dataset_disclaimer") or DISCLAIMER,
    }


def recommend(pillar: str, jurisdiction: str = "US", population: str = "adult", patient: dict | None = None) -> dict:
    """Return guideline-cited recommendation(s) for a scenario.

    Args:
        pillar: one of PILLARS.
        jurisdiction: "US" or "UK".
        population: "adult", "adolescent", or "child".
        patient: optional dict with any of TRIGGER_KEYS (e.g. {"penicillin_allergy": "severe"}).

    Returns a dict with the ranked matching rules, the inputs that would sharpen the match,
    and a disclaimer. Never returns a prescription — always a cited reference.
    """
    if pillar not in PILLARS:
        raise ValueError(f"Unknown pillar '{pillar}'. Options: {', '.join(PILLARS)}")
    patient = {k: v for k, v in (patient or {}).items() if v is not None}
    sources = load_sources()

    candidates = [
        r for r in load_rules()
        if r["pillar"] == pillar
        and r["jurisdiction"] == jurisdiction
        and _pop_match(r.get("population", {}).get("group", "all"), population)
    ]

    scored, missing_all = [], set()
    for r in candidates:
        triggers = r.get("scenario", {}).get("triggers", {})
        compatible, matched, missing = _evaluate(triggers, patient)
        if not compatible:
            continue
        scored.append((matched, -len(missing), r))
        missing_all.update(missing)

    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    results = [_format(r, sources) for _, _, r in scored]

    # inputs that would disambiguate the top candidates
    top_score = scored[0][0] if scored else 0
    needed = sorted({
        k for m, _, r in scored if m == top_score
        for k in r.get("scenario", {}).get("triggers", {})
        if k not in patient
    })

    return {
        "query": {"pillar": pillar, "jurisdiction": jurisdiction, "population": population, "patient": patient},
        "results": results,
        "needs_input": needed,
        "disclaimer": DISCLAIMER,
    }
