# Cyrisk Controls

> **Versioned synthetic control-effect and cost-assumption comparison records—not causal analysis, ROI calculation, pricing research, procurement advice, or a control-performance claim.**

`cyrisk-controls` provides typed, immutable records that bind a supplied control option and its
synthetic cost/effect ranges to two supplied scenario summaries. It calculates an arithmetic
comparison of those supplied summaries and attaches limitations. It does not fetch pricing, inspect
a control, measure outcomes, or infer causation.

| Artifact | Deterministic purpose | Explicit non-claim |
|---|---|---|
| `ControlAssumption` | Versioned supplied cost/effect range and evidence-reference metadata. | Not a validated price or effectiveness estimate. |
| `ScenarioSummary` | Sealed summary range supplied by a caller. | Not a loss forecast. |
| `ComparisonRequest` | Binds baseline and candidate summaries to a control assumption. | Not an experiment or causal study. |
| `ControlComparison` | Arithmetic delta and manifest hash. | Not ROI, savings, or purchase advice. |

`make check` validates the sealed synthetic fixture, strict types, full test coverage, and wheel
contents. The library has no network client, cloud SDK, database, scheduler, or hosted runtime.

## Boundary

Any downstream decision owner must validate financial assumptions, tax/accounting treatment,
currency, budget, procurement, legal terms, deployment, control operation, performance, and
authority. A lower synthetic candidate range is only a comparison of caller-supplied records.
