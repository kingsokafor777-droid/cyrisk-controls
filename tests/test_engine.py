from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from cyrisk_controls.engine import compare
from cyrisk_controls.models import ComparisonRequest

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_control_comparison.json"


def request() -> ComparisonRequest:
    return ComparisonRequest.model_validate_json(FIXTURE.read_text(encoding="utf-8"))


def test_comparison_is_deterministic_and_explicitly_non_causal() -> None:
    result = compare(request())
    assert result.central_delta == Decimal("70000")
    assert result.cost_central == Decimal("15000")
    assert result.non_causal is True
    assert "not causal" in result.limitations


def test_manifest_hash_changes_when_supplied_input_changes() -> None:
    baseline = compare(request())
    payload = request().model_dump(mode="json")
    payload["candidate"]["central"] = "170000"  # type: ignore[index]
    changed = compare(ComparisonRequest.model_validate(payload))
    assert changed.manifest_hash != baseline.manifest_hash
    assert changed.central_delta == Decimal("80000")
