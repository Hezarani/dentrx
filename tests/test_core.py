"""Guideline-anchored tests for the DentRx engine.

Each test asserts a fact that is traceable to docs/EVIDENCE.md and the primary source.
These are the hand-verified anchors that a DDS signs off before release.
"""

import json
from pathlib import Path

import pytest

from dentrx import recommend, load_rules, load_sources, pillars, DISCLAIMER

ROOT = Path(__file__).resolve().parent.parent


def _all_drugs(res):
    drugs = []
    for r in res["results"]:
        for opt in r["recommendation"].get("options", []):
            for c in opt.get("components", []):
                drugs.append(c.get("drug", "").lower())
    return " | ".join(drugs)


def _actions(res):
    return {r["recommendation"].get("action") for r in res["results"]}


# ---- structural integrity -------------------------------------------------

def test_every_rule_has_citation_and_disclaimer():
    sources = load_sources()
    for r in load_rules():
        assert r.get("sources"), f"{r['id']} has no source"
        for s in r["sources"]:
            assert s in sources, f"{r['id']} references unknown source {s}"
        assert r.get("_dataset_disclaimer"), f"{r['id']} missing disclaimer"


def test_pillars_present():
    assert set(pillars()) == {
        "analgesia", "prophylaxis_ie", "prophylaxis_joint", "therapeutic_infection"
    }


def test_no_cdt_codes_anywhere():
    # ADA CDT codes look like D#### — must never appear in the datasets.
    import re
    blob = ""
    for f in (ROOT / "data").glob("*.json"):
        blob += f.read_text(encoding="utf-8")
    assert not re.search(r"\bD\d{4}\b", blob), "A CDT-like code appears in the data"


# ---- analgesia ------------------------------------------------------------

def test_us_adult_analgesia_first_line_is_nsaid():
    res = recommend("analgesia", "US", "adult")
    drugs = _all_drugs(res)
    assert "ibuprofen" in drugs and "acetaminophen" in drugs
    # ibuprofen daily ceiling per ADA 2024
    text = json.dumps(res)
    assert "2400 mg" in text


def test_child_codeine_tramadol_contraindicated():
    res = recommend("analgesia", "US", "child")
    ids = [r["id"] for r in res["results"]]
    assert "us.analgesia.child.opioids_contraindicated" in ids
    contra = next(r for r in res["results"] if r["id"].endswith("opioids_contraindicated"))
    assert contra["recommendation"]["action"] == "do_not_prescribe"
    blob = json.dumps(contra).lower()
    assert "codeine" in blob and "tramadol" in blob


# ---- IE prophylaxis -------------------------------------------------------

def test_ie_standard_adult_amoxicillin_2g():
    res = recommend("prophylaxis_ie", "US", "adult",
                    {"cardiac_highest_risk": True, "penicillin_allergy": "none", "can_take_oral": True})
    top = res["results"][0]
    assert top["recommendation"]["action"] == "prescribe"
    drugs = _all_drugs(res)
    assert "amoxicillin" in drugs
    assert "2 g" in json.dumps(top)


def test_ie_severe_allergy_excludes_cephalosporin():
    res = recommend("prophylaxis_ie", "US", "adult",
                    {"cardiac_highest_risk": True, "penicillin_allergy": "severe", "can_take_oral": True})
    drugs = _all_drugs(res)
    assert "cephalexin" not in drugs, "cephalosporin must not appear for severe penicillin allergy"
    assert ("azithromycin" in drugs) or ("doxycycline" in drugs)


def test_ie_not_indicated_when_not_highest_risk():
    res = recommend("prophylaxis_ie", "US", "adult", {"cardiac_highest_risk": False})
    assert "do_not_prescribe" in _actions(res)
    assert "prescribe" not in _actions(res)


def test_ie_clindamycin_never_recommended():
    for pop in ("adult", "child"):
        for allergy in ("non_severe", "severe"):
            res = recommend("prophylaxis_ie", "US", pop,
                            {"cardiac_highest_risk": True, "penicillin_allergy": allergy, "can_take_oral": True})
            assert "clindamycin" not in _all_drugs(res)


# ---- prosthetic joint -----------------------------------------------------

def test_prosthetic_joint_do_not_prescribe():
    for j in ("US", "UK"):
        res = recommend("prophylaxis_joint", j, "adult", {"prosthetic_joint": True})
        assert _actions(res) == {"do_not_prescribe"}


# ---- therapeutic infection ------------------------------------------------

def test_therapeutic_no_systemic_is_definitive_treatment():
    res = recommend("therapeutic_infection", "US", "adult", {"systemic_involvement": False})
    assert "definitive_dental_treatment" in _actions(res)


def test_therapeutic_systemic_us_amoxicillin():
    res = recommend("therapeutic_infection", "US", "adult",
                    {"systemic_involvement": True, "penicillin_allergy": "none"})
    drugs = _all_drugs(res)
    assert "amoxicillin" in drugs
    assert "penicillin v" in drugs


def test_therapeutic_systemic_severe_allergy_macrolide_only():
    res = recommend("therapeutic_infection", "US", "adult",
                    {"systemic_involvement": True, "penicillin_allergy": "severe"})
    drugs = _all_drugs(res)
    assert ("azithromycin" in drugs) or ("clarithromycin" in drugs)
    assert "cephalexin" not in drugs


def test_therapeutic_uk_first_line():
    res = recommend("therapeutic_infection", "UK", "adult",
                    {"systemic_involvement": True, "penicillin_allergy": "none"})
    drugs = _all_drugs(res)
    assert "amoxicillin" in drugs
    assert "phenoxymethylpenicillin" in drugs


def test_needs_input_surfaced_when_underspecified():
    res = recommend("prophylaxis_ie", "US", "adult", {"cardiac_highest_risk": True})
    # engine should ask for allergy / oral-route to disambiguate
    assert "penicillin_allergy" in res["needs_input"] or "can_take_oral" in res["needs_input"]


def test_disclaimer_always_present():
    res = recommend("analgesia", "US", "adult")
    assert res["disclaimer"] == DISCLAIMER


# ---- audit fixes (regression tests) --------------------------------------

def test_uk_therapeutic_non_severe_allergy_is_covered():
    # audit issue #1: UK non-severe penicillin allergy must not return an empty result
    res = recommend("therapeutic_infection", "UK", "adult",
                    {"systemic_involvement": True, "penicillin_allergy": "non_severe"})
    assert res["results"], "UK non-severe allergy returned no guidance"
    drugs = _all_drugs(res)
    assert ("clarithromycin" in drugs) or ("metronidazole" in drugs)
    assert "amoxicillin" not in drugs and "phenoxymethylpenicillin" not in drugs


def test_ie_severe_allergy_unable_oral_refers_safely():
    # audit issue #2: no bare "prescribe []" — must surface a refer/advice action
    res = recommend("prophylaxis_ie", "US", "adult",
                    {"cardiac_highest_risk": True, "penicillin_allergy": "severe", "can_take_oral": False})
    assert "refer" in _actions(res)
    assert "cephalexin" not in _all_drugs(res) and "clindamycin" not in _all_drugs(res)


def test_ie_child_unable_oral_covered():
    # audit issue #3
    res = recommend("prophylaxis_ie", "US", "child",
                    {"cardiac_highest_risk": True, "penicillin_allergy": "none", "can_take_oral": False})
    drugs = _all_drugs(res)
    assert "ampicillin" in drugs


def test_adolescent_gets_opioid_caution_but_adult_does_not():
    # audit issue #4
    ado = recommend("analgesia", "US", "adolescent")
    assert any(r["id"].endswith("adolescent.opioid_caution") for r in ado["results"])
    assert "ibuprofen" in _all_drugs(ado)  # still first-line NSAID
    adult = recommend("analgesia", "US", "adult")
    assert not any("adolescent" in r["id"] for r in adult["results"])


def test_us_therapeutic_severe_matches_ada2019_agents():
    # audit issue #5: azithromycin + clindamycin are the guideline agents; no cephalosporin
    res = recommend("therapeutic_infection", "US", "adult",
                    {"systemic_involvement": True, "penicillin_allergy": "severe"})
    drugs = _all_drugs(res)
    assert "azithromycin" in drugs and "clindamycin" in drugs
    assert "cephalexin" not in drugs


def test_analgesia_first_line_ranks_above_opioid_reserve():
    # UI review: first-line NSAID must be the headline card for acute pain, not opioids
    res = recommend("analgesia", "US", "adult")
    assert res["results"], "no analgesia result"
    assert res["results"][0]["id"] == "us.analgesia.adult.first_line"
    # analgesia must not prompt for penicillin allergy (it doesn't depend on it)
    assert "penicillin_allergy" not in res["needs_input"]
