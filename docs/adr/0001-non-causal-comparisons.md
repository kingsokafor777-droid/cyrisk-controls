# ADR 0001: Make comparisons explicitly non-causal

**Status:** Accepted

The component computes arithmetic differences between supplied synthetic scenario summaries and
stores a required `non_causal=true` flag. It does not treat two records as a controlled experiment,
estimate causal effects, calculate ROI, or recommend purchase. This prevents a portfolio artifact
from implying evidence it does not possess.
