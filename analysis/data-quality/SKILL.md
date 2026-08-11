---
name: data-quality
description: Run a structured data quality assessment across completeness, validity, consistency, timeliness, and uniqueness, producing a per-dimension verdict rather than a single score. Use before trusting a dataset for reporting or before migrating it between systems.
metadata:
  version: "1.0"
---

# Data Quality Assessment

This skill lives in a nested category folder (`analysis/data-quality/`) rather
than at the repository root. Discovery is layout-agnostic, so nesting is a way
to organise a growing catalog without changing how skills are addressed.

## When to use this

- Before a dataset becomes the basis for reporting anyone acts on
- Before migrating data between systems, where quality problems get copied
  and then blamed on the migration
- When two systems disagree about a number that should match

## The five dimensions

Assess each separately and give each its own verdict. Do not average them
into one score — a dataset that is perfectly complete and entirely stale is
not "70% good", it is unusable for anything time-sensitive and fine for
historical work. The shape of the failure is the useful part.

1. **Completeness** — are required fields populated? Distinguish "missing"
   from "legitimately empty"; an empty `cancelled_at` on an active order is
   correct, not missing.

2. **Validity** — do values conform to their domain? Types, ranges, enums,
   formats. A `country` of `XX` is present but not valid.

3. **Consistency** — do related values agree, within this dataset and against
   others? `created_at` after `updated_at` is an internal inconsistency;
   a total that disagrees with the sum of its line items is a cross-record one.

4. **Timeliness** — how stale is it, relative to the decision it will inform?
   State the age and the freshness requirement separately, because staleness
   only means something against a requirement.

5. **Uniqueness** — are there duplicates? Say what key you deduplicated on,
   since "duplicate" is meaningless without one.

## Output

Per dimension: verdict (`pass` / `concern` / `fail`), the evidence, and the
decisions it blocks. Close with the single highest-impact remediation rather
than an exhaustive list — a long list of equally-weighted findings tends to
produce no action at all.
