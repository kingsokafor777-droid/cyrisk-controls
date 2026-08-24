"""Generate a sealed synthetic Cyrisk Controls comparison request."""

from __future__ import annotations

from pathlib import Path

from cyrisk_controls.models import ComparisonRequest

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "fixtures" / "synthetic_control_comparison.json"
RUN_HASH = "9cda1845c4a1f3dbdb61ec074bf2c7d63dfa19501dcd8636b96e5a5cf014c696"

PAYLOAD = {
    "comparison_id": "comparison-synthetic-ransomware",
    "baseline": {
        "summary_id": "summary-baseline",
        "scenario_id": "scenario-synthetic-ransomware",
        "currency": "USD",
        "central": "250000",
        "run_hash": RUN_HASH,
        "limitations": "Sealed synthetic scenario summary only.",
    },
    "candidate": {
        "summary_id": "summary-candidate",
        "scenario_id": "scenario-synthetic-ransomware",
        "currency": "USD",
        "central": "180000",
        "run_hash": RUN_HASH,
        "limitations": "Sealed synthetic scenario summary only.",
    },
    "control": {
        "control_id": "control-mfa-synthetic",
        "version": "1.0",
        "name": "Synthetic MFA control assumption",
        "effect_dimension": "frequency",
        "effect_lower": "0.05",
        "effect_central": "0.15",
        "effect_upper": "0.30",
        "cost": {
            "currency": "USD",
            "basis": "annual",
            "lower": "10000",
            "central": "15000",
            "upper": "25000",
        },
        "evidence_reference": "synthetic-evidence-control",
        "rationale": "Sealed synthetic assumption; no vendor or causal claim.",
        "non_causal": True,
    },
}


def main() -> None:
    request = ComparisonRequest.model_validate(PAYLOAD)
    TARGET.write_text(request.model_dump_json(indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
