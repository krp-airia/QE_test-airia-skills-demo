---
name: csv-insights
description: Profile a CSV file before analysing it — row and column counts, inferred types, null density, cardinality, and outlier flags. Use when someone hands over tabular data and you need to understand its shape and trustworthiness before drawing conclusions from it.
metadata:
  version: "1.0"
---

# CSV Insights

Profiling comes before analysis. A column that is 60% null or that silently
mixes two units will produce a confident, wrong answer if you chart it first
and inspect it never.

## When to use this

- Someone attaches a `.csv` and asks a question about its contents
- You are about to aggregate, join, or chart a dataset you have not seen
- A result looks surprising and you need to rule out data quality first

## Procedure

1. **Shape.** Report row count, column count, and file size. If the row count
   is under 30, say so — most summary statistics stop meaning much below that.

2. **Per column, report:**
   - Inferred type, and whether inference was ambiguous
   - Null count and percentage
   - Cardinality — flag columns where every value is unique (likely an ID) or
     where one value covers more than 90% of rows (likely near-constant)
   - For numerics: min, median, max, and count of values beyond 3 standard
     deviations

3. **Flag before interpreting.** Surface these as caveats *before* answering
   the user's actual question, not as a footnote after it:
   - Any column above 30% null
   - Mixed types within one column
   - Dates parsed under more than one format
   - Numeric columns stored as text

4. **Answer the question** the user actually asked, with the caveats attached
   to whichever conclusions they affect.

## Running the profiler

`scripts/profile.py` does steps 1 and 2 and prints a summary table:

```
python scripts/profile.py <path-to-csv>
```

It uses only the standard library, so it runs anywhere without installation.
For files above roughly 100 MB, sample rather than loading whole — the script
takes an optional `--sample N` argument for this.

## What not to do

Do not silently drop null rows to make a statistic computable. Report the
null count and let the user decide whether dropping is acceptable, because
whether missingness is random is a question about the world, not the data.
