# Incident Timeline — output format

Supporting file for the `incident-timeline` skill. Fetched on demand when the
skill is activated, not loaded during discovery.

## Table format

| Time (UTC) | Class | Source | Event |
|---|---|---|---|
| 14:02:11 | OBSERVED | `api-gw` logs | 5xx rate crosses 2% |
| 14:04:00 | INFERRED | — | Connection pool likely saturated |
| 14:06:38 | OBSERVED | PagerDuty | On-call paged |
| 14:09:15 | REPORTED | #incident | "Started seeing timeouts around 14:00" |
| 14:31:02 | OBSERVED | deploy log | Rollback to `v2.4.1` completes |

Keep the class column adjacent to the time column. It is the column readers
skip when it is placed last, and it is the one that keeps the timeline honest.

## Anchors block

State the four anchors above the table, with explicit unknowns:

```
First impact:  14:00:00 UTC (approx — inferred from 5xx onset)
Detection:     14:06:38 UTC
Mitigation:    14:31:02 UTC
Resolution:    unknown — root cause fix not yet shipped
```

## Duration arithmetic

Report two durations, and do not conflate them:

- **Time to detect** — first impact to detection
- **Time to mitigate** — first impact to mitigation, *not* detection to
  mitigation

Measuring from detection flatters the response by hiding the undetected
window, which is usually the part worth improving.

## Worked example

An outage where detection lagged impact by six minutes and mitigation took a
further 25:

```
First impact:  14:00:00 UTC (approx)
Detection:     14:06:38 UTC   → time to detect: ~6m 38s
Mitigation:    14:31:02 UTC   → time to mitigate: ~31m 02s
Resolution:    2026-08-02 09:15:00 UTC
```

The gap between 14:09 and 14:31 has no `OBSERVED` entries. That is a finding
in itself — the response was happening but was not being recorded anywhere
durable, so it cannot be reviewed.
