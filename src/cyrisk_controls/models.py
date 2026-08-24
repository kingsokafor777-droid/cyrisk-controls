"""Strict contracts for supplied synthetic control comparison artifacts."""

from __future__ import annotations

from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

ID_PATTERN = r"^[a-z][a-z0-9_-]{2,63}$"
HASH_PATTERN = r"^[a-f0-9]{64}$"


class ControlRecord(BaseModel):
    """Immutable strict record shared by all public controls artifacts."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class CostBasis(str, Enum):
    ANNUAL = "annual"
    ONE_TIME = "one_time"


class EffectDimension(str, Enum):
    FREQUENCY = "frequency"
    IMPACT = "impact"
    EXPOSURE = "exposure"


class CostRange(ControlRecord):
    """Supplied synthetic cost range with explicit currency and basis."""

    currency: str = Field(pattern=r"^[A-Z]{3}$")
    basis: CostBasis
    lower: Decimal = Field(ge=0)
    central: Decimal = Field(ge=0)
    upper: Decimal = Field(ge=0)

    @model_validator(mode="after")
    def validate_bounds(self) -> CostRange:
        if not self.lower <= self.central <= self.upper:
            raise ValueError("cost bounds must satisfy lower <= central <= upper")
        return self


class ControlAssumption(ControlRecord):
    """Versioned supplied control-effect/cost assumption with no causal semantics."""

    control_id: str = Field(pattern=ID_PATTERN)
    version: str = Field(pattern=r"^\d+\.\d+$")
    name: str = Field(min_length=1, max_length=160)
    effect_dimension: EffectDimension
    effect_lower: Decimal = Field(ge=0, le=1)
    effect_central: Decimal = Field(ge=0, le=1)
    effect_upper: Decimal = Field(ge=0, le=1)
    cost: CostRange
    evidence_reference: str = Field(min_length=1, max_length=160)
    rationale: str = Field(min_length=1, max_length=500)
    non_causal: bool = True

    @model_validator(mode="after")
    def validate_non_causal_effect_range(self) -> ControlAssumption:
        if not self.effect_lower <= self.effect_central <= self.effect_upper:
            raise ValueError("effect bounds must satisfy lower <= central <= upper")
        if not self.non_causal:
            raise ValueError("control assumptions must remain explicitly non-causal")
        return self


class ScenarioSummary(ControlRecord):
    """Caller-supplied scenario summary; not a model execution or forecast."""

    summary_id: str = Field(pattern=ID_PATTERN)
    scenario_id: str = Field(pattern=ID_PATTERN)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    central: Decimal = Field(ge=0)
    run_hash: str = Field(pattern=HASH_PATTERN)
    limitations: str = Field(min_length=1, max_length=500)


class ComparisonRequest(ControlRecord):
    """Binds two supplied summaries and one control assumption for arithmetic comparison."""

    comparison_id: str = Field(pattern=ID_PATTERN)
    baseline: ScenarioSummary
    candidate: ScenarioSummary
    control: ControlAssumption

    @model_validator(mode="after")
    def validate_comparable_summaries(self) -> ComparisonRequest:
        if self.baseline.currency != self.candidate.currency:
            raise ValueError("baseline and candidate currency must match")
        if self.baseline.summary_id == self.candidate.summary_id:
            raise ValueError("baseline and candidate summary_id must differ")
        return self


class ControlComparison(ControlRecord):
    """A reproducible non-causal arithmetic comparison with explicit limitations."""

    comparison_id: str = Field(pattern=ID_PATTERN)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    baseline_central: Decimal = Field(ge=0)
    candidate_central: Decimal = Field(ge=0)
    central_delta: Decimal
    cost_central: Decimal = Field(ge=0)
    cost_basis: CostBasis
    control_id: str = Field(pattern=ID_PATTERN)
    control_version: str = Field(pattern=r"^\d+\.\d+$")
    manifest_hash: str = Field(pattern=HASH_PATTERN)
    non_causal: bool = True
    limitations: str = Field(min_length=1, max_length=500)

    @model_validator(mode="after")
    def validate_non_causal_output(self) -> ControlComparison:
        if not self.non_causal:
            raise ValueError("comparison output must remain explicitly non-causal")
        return self
