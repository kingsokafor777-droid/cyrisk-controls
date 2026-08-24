from __future__ import annotations

import pytest
from pydantic import ValidationError

from cyrisk_controls.models import (
    ComparisonRequest,
    ControlAssumption,
    ControlComparison,
    CostRange,
)


def control() -> dict[str, object]:
    return {
        "control_id": "control-one",
        "version": "1.0",
        "name": "Synthetic control",
        "effect_dimension": "frequency",
        "effect_lower": "0.1",
        "effect_central": "0.2",
        "effect_upper": "0.3",
        "cost": {"currency": "USD", "basis": "annual", "lower": "1", "central": "2", "upper": "3"},
        "evidence_reference": "synthetic-evidence",
        "rationale": "Synthetic rationale.",
        "non_causal": True,
    }


def summary(summary_id: str, currency: str = "USD") -> dict[str, object]:
    return {
        "summary_id": summary_id,
        "scenario_id": "scenario-one",
        "currency": currency,
        "central": "100",
        "run_hash": "a" * 64,
        "limitations": "Synthetic summary.",
    }


def payload() -> dict[str, object]:
    return {
        "comparison_id": "comparison-one",
        "baseline": summary("summary-one"),
        "candidate": summary("summary-two"),
        "control": control(),
    }


def test_cost_and_effect_ranges_reject_reversed_values() -> None:
    with pytest.raises(ValidationError, match="cost bounds"):
        CostRange(currency="USD", basis="annual", lower="3", central="2", upper="1")
    record = control()
    record["effect_lower"] = "0.4"
    with pytest.raises(ValidationError, match="effect bounds"):
        ControlAssumption.model_validate(record)


def test_control_rejects_causal_assertion() -> None:
    record = control()
    record["non_causal"] = False
    with pytest.raises(ValidationError, match="non-causal"):
        ControlAssumption.model_validate(record)


def test_request_rejects_currency_mismatch_and_duplicate_summary() -> None:
    request = payload()
    request["candidate"] = summary("summary-two", "CAD")
    with pytest.raises(ValidationError, match="currency"):
        ComparisonRequest.model_validate(request)
    request = payload()
    request["candidate"] = summary("summary-one")
    with pytest.raises(ValidationError, match="must differ"):
        ComparisonRequest.model_validate(request)


def test_comparison_output_rejects_causal_assertion() -> None:
    with pytest.raises(ValidationError, match="explicitly non-causal"):
        ControlComparison(
            comparison_id="comparison-one",
            currency="USD",
            baseline_central="100",
            candidate_central="90",
            central_delta="10",
            cost_central="5",
            cost_basis="annual",
            control_id="control-one",
            control_version="1.0",
            manifest_hash="a" * 64,
            non_causal=False,
            limitations="Synthetic comparison only.",
        )
