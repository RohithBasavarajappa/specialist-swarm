---
name: deal-history-comparison
description: Compare an inbound RFP with same-vendor deals, recent wins, and the most similar historical deal. Surface deviations in commercial, legal, technical, and competitive requirements and recommend evidence-based actions.
---

# Deal History Comparison

Use `past-wins.json` as the source of truth for historical benchmarks. Do not invent values that are not present in the RFP or deal history.

## Comparison set

Select and explicitly name:

1. Same-vendor or same-competitor-pattern deals, especially deals involving Snowflake, Databricks, or Microsoft Fabric.
2. The most recent wins by close date.
3. The most similar deal by industry, scale, tier, requirements, and competitive context.

A single deal may serve more than one comparison role, but explain why.

## Required diff

Compare the current RFP and selected deals across:

- Industry, scale, tier, and term
- Annual value, list-price discount, and payment terms
- Competitors and the reason the historical deal was won or lost
- SLA and performance expectations
- Liability, termination, audit, IP, and other legal positions
- Delivery, geography, data residency, and implementation requirements

For every field, label the RFP as **more demanding**, **less demanding**, **in line**, or **unknown** relative to the comparison deal. Include the historical evidence and call out missing data instead of guessing.

## Output format

Return:

1. **Comparison set**: deal, role, and selection rationale.
2. **Benchmark diff**: a compact table with field, historical benchmark, RFP requirement, deviation, and evidence.
3. **Key deviations**: the three to five changes most likely to affect price, margin, risk, or win probability.
4. **Recommended actions**: specific asks or concessions for Pricing, Legal, Technical Fit, and the coordinator.

Keep the report concise and decision-oriented. Distinguish facts from inferences.
