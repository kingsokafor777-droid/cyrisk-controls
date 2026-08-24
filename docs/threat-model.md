# Threat Model

| Threat | Example | Mitigation and boundary |
|---|---|---|
| Causal overclaim | A range delta is marketed as a realized saving. | `non_causal=true` is required; limitations are emitted. |
| Pricing leakage | A fixture contains a vendor quote. | Synthetic input policy and no external fetcher. |
| Unit ambiguity | A cost range mixes currency/time basis. | Cost basis and currency must be explicit. |
| Hidden substitution | A supplied control range changes after review. | Canonical manifest hashing exposes mutation. |
| Unauthorized decision | A comparison triggers a purchase. | No approval, procurement, or execution capability exists. |
