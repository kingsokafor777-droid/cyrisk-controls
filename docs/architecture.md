# Architecture

The package is local-first and pure. A caller supplies a control assumption and two sealed scenario
summaries. The comparison function calculates `baseline_central - candidate_central` and returns a
manifest hash, explicit inputs, and a limitation statement. It does not run a model or inspect a
control.

| Stage | Input | Output | Boundary |
|---|---|---|---|
| Register | Synthetic cost/effect range | `ControlAssumption` | Does not validate a commercial quote. |
| Compare | Two supplied scenario summaries | `ControlComparison` | Does not infer causal reduction. |
| Seal | Canonical JSON | SHA-256 manifest hash | Does not prove operational truth. |
| Review | Caller-owned workflow | Optional downstream evidence | This package never approves a decision. |
