"""DentRx command-line interface.

Examples:
    dentrx pillars
    dentrx recommend --pillar analgesia --jurisdiction US --population adult
    dentrx recommend -p prophylaxis_ie -j US --cardiac-highest-risk --allergy severe
    dentrx recommend -p therapeutic_infection -j UK --systemic --allergy none
"""

from __future__ import annotations

import argparse
import json
import sys

from .core import recommend, pillars, load_sources, DISCLAIMER, __version__


def _bar(width=64):
    return "─" * width


def _print_result(res: dict) -> None:
    q = res["query"]
    print(_bar())
    print(f"DentRx · {pillars().get(q['pillar'], q['pillar'])}  [{q['jurisdiction']} · {q['population']}]")
    print(_bar())
    if not res["results"]:
        print("No matching rule for these inputs. Try adding patient details or check the jurisdiction.")
    for i, r in enumerate(res["results"], 1):
        rec = r["recommendation"]
        action = rec.get("action", "").replace("_", " ").upper()
        print(f"\n[{i}] {action}  ({r['status']})")
        if rec.get("summary"):
            print(f"    {rec['summary']}")
        for opt in rec.get("options", []):
            label = opt.get("label", opt.get("regimen_id", "option"))
            print(f"    • {label}")
            for c in opt.get("components", []):
                bits = [c.get("drug", "")]
                for key in ("dose", "route", "frequency", "duration", "timing", "max_daily"):
                    if c.get(key):
                        bits.append(f"{key}={c[key]}")
                print("        - " + ", ".join(b for b in bits if b))
            if opt.get("notes"):
                print(f"        ({opt['notes']})")
        if r.get("contraindications"):
            print("    Contraindications: " + "; ".join(r["contraindications"]))
        if r.get("cautions"):
            print("    Cautions: " + "; ".join(r["cautions"]))
        if r.get("rationale"):
            print(f"    Why: {r['rationale']}")
        for cit in r.get("citations", []):
            line = cit.get("citation") or cit.get("title") or cit["key"]
            if cit.get("url"):
                line += f"  <{cit['url']}>"
            print(f"    Source: {line}")
    if res.get("needs_input"):
        print(f"\nProvide for a sharper match: {', '.join(res['needs_input'])}")
    print("\n" + DISCLAIMER)
    print(_bar())


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="dentrx", description="Guideline-cited dental prescribing reference (educational, not a prescription).")
    p.add_argument("--version", action="version", version=f"dentrx {__version__}")
    sub = p.add_subparsers(dest="command")

    sub.add_parser("pillars", help="List available clinical pillars.")
    sub.add_parser("sources", help="List the authoritative sources with DOIs/URLs.")

    r = sub.add_parser("recommend", help="Return a cited recommendation.")
    r.add_argument("-p", "--pillar", required=True, choices=list(pillars()))
    r.add_argument("-j", "--jurisdiction", default="US", choices=["US", "UK"])
    r.add_argument("-a", "--population", default="adult", choices=["adult", "adolescent", "child"])
    r.add_argument("--allergy", choices=["none", "non_severe", "severe"], help="Penicillin allergy status.")
    r.add_argument("--systemic", action="store_true", help="Systemic involvement (fever/malaise) present.")
    r.add_argument("--cardiac-highest-risk", action="store_true", help="Highest-risk cardiac condition present.")
    r.add_argument("--prosthetic-joint", action="store_true", help="Patient has a prosthetic joint.")
    r.add_argument("--no-oral", action="store_true", help="Patient cannot take oral medication.")
    r.add_argument("--json", action="store_true", help="Emit raw JSON.")

    args = p.parse_args(argv)

    if args.command == "pillars":
        for k, v in pillars().items():
            print(f"{k:24} {v}")
        return 0

    if args.command == "sources":
        for key, s in load_sources().items():
            print(f"{key}\n    {s.get('citation','')}\n    {s.get('url','')}")
        return 0

    if args.command == "recommend":
        patient = {}
        if args.allergy:
            patient["penicillin_allergy"] = args.allergy
        if args.systemic:
            patient["systemic_involvement"] = True
        if args.cardiac_highest_risk:
            patient["cardiac_highest_risk"] = True
        if args.prosthetic_joint:
            patient["prosthetic_joint"] = True
        if args.no_oral:
            patient["can_take_oral"] = False
        res = recommend(args.pillar, args.jurisdiction, args.population, patient)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            _print_result(res)
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
