"""Pure deterministic arithmetic comparison over supplied synthetic records."""

from __future__ import annotations

from cyrisk_core.canonical import content_hash

from cyrisk_controls.models import ComparisonRequest, ControlComparison

LIMITATIONS = (
    "Arithmetic comparison of supplied synthetic summaries and supplied control assumptions only; "
    "not causal evidence, realized savings, ROI, pricing validation, or a decision recommendation."
)


def compare(request: ComparisonRequest) -> ControlComparison:
    """Return a hash-bound non-causal delta between caller-supplied scenario summaries."""
    manifest_hash = content_hash(request.model_dump(mode="json"))
    return ControlComparison(
        comparison_id=request.comparison_id,
        currency=request.baseline.currency,
        baseline_central=request.baseline.central,
        candidate_central=request.candidate.central,
        central_delta=request.baseline.central - request.candidate.central,
        cost_central=request.control.cost.central,
        cost_basis=request.control.cost.basis,
        control_id=request.control.control_id,
        control_version=request.control.version,
        manifest_hash=manifest_hash,
        limitations=LIMITATIONS,
    )
