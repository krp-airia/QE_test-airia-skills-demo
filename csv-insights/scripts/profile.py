#!/usr/bin/env python3
"""Profile a CSV: shape, types, null density, cardinality, outliers.

Standard library only, so it runs without installation. Supporting file for
the csv-insights skill — fetched on demand by the host, not bundled.
"""

import argparse
import csv
import math
import statistics
import sys
from collections import Counter


def infer_type(values):
    """Return the narrowest type that fits every non-empty value."""
    seen = set()
    for value in values:
        if value == "":
            continue
        try:
            int(value)
            seen.add("int")
            continue
        except ValueError:
            pass
        try:
            float(value)
            seen.add("float")
            continue
        except ValueError:
            pass
        seen.add("str")

    if not seen:
        return "empty"
    if seen == {"int"}:
        return "int"
    if seen <= {"int", "float"}:
        return "float"
    if len(seen) > 1:
        return "mixed"
    return "str"


def outlier_count(values):
    """Count values more than 3 standard deviations from the mean."""
    numbers = []
    for value in values:
        try:
            numbers.append(float(value))
        except ValueError:
            continue

    if len(numbers) < 2:
        return 0

    mean = statistics.fmean(numbers)
    sigma = statistics.pstdev(numbers)
    if math.isclose(sigma, 0.0):
        return 0

    return sum(1 for n in numbers if abs(n - mean) > 3 * sigma)


def profile(path, sample=None):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            print(f"{path}: no header row found", file=sys.stderr)
            return 1

        columns = {name: [] for name in reader.fieldnames}
        rows = 0
        for row in reader:
            rows += 1
            for name in reader.fieldnames:
                columns[name].append((row.get(name) or "").strip())
            if sample and rows >= sample:
                break

    print(f"{path}\n{rows} rows x {len(columns)} columns")
    if rows < 30:
        print("NOTE: fewer than 30 rows — summary statistics are weak here.")
    print()

    header = f"{'column':<24} {'type':<8} {'null%':>7} {'unique':>8} {'outliers':>9}"
    print(header)
    print("-" * len(header))

    for name, values in columns.items():
        kind = infer_type(values)
        nulls = sum(1 for v in values if v == "")
        null_pct = (nulls / rows * 100) if rows else 0.0
        unique = len(Counter(values))
        outliers = outlier_count(values) if kind in ("int", "float") else 0

        flag = ""
        if null_pct > 30:
            flag = "  <-- high null density"
        elif kind == "mixed":
            flag = "  <-- mixed types"
        elif rows and unique == rows:
            flag = "  <-- unique per row (likely an ID)"

        print(
            f"{name[:24]:<24} {kind:<8} {null_pct:>6.1f}% "
            f"{unique:>8} {outliers:>9}{flag}"
        )

    return 0


def main():
    parser = argparse.ArgumentParser(description="Profile a CSV file.")
    parser.add_argument("path", help="Path to the CSV file")
    parser.add_argument(
        "--sample",
        type=int,
        default=None,
        help="Read at most N rows (use for very large files)",
    )
    args = parser.parse_args()
    return profile(args.path, args.sample)


if __name__ == "__main__":
    sys.exit(main())
