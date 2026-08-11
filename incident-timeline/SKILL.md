---
name: incident-timeline
description: Reconstruct an incident timeline from logs, alerts, and chat transcripts into a single ordered narrative with UTC timestamps, separating what was observed from what was inferred. Use when writing a postmortem or when someone asks what happened during an outage.
metadata:
  version: "1.0"
---

# Incident Timeline

The hard part of a postmortem is not finding events. It is keeping the order
honest — separating what was observed at a time from what was later inferred
about that time.

## When to use this

- Writing or reviewing a postmortem
- Someone asks "what actually happened" about a past outage
- Reconciling accounts from several sources that disagree

## Procedure

1. **Normalise every timestamp to UTC** and note the original zone in
   parentheses. Mixed zones are the single most common source of a wrong
   timeline, and they fail quietly because the ordering still looks plausible.

2. **Classify each entry** into exactly one of:
   - `OBSERVED` — appears in a log, alert, or message with its own timestamp
   - `INFERRED` — deduced afterwards, including anything reconstructed from a
     later state
   - `REPORTED` — a human account given after the fact, timestamped by when
     the event allegedly happened, not when it was reported

3. **Order by timestamp**, keeping the classification visible on every row.
   Never promote `INFERRED` to `OBSERVED` because it fits the story well.

4. **Mark the four anchors** explicitly, and say when one is unknown rather
   than estimating it:
   - First impact — when users were first affected, which usually precedes
     detection
   - Detection — when a human or alert first knew
   - Mitigation — when impact stopped
   - Resolution — when the cause was fixed, often much later

5. **Note the gaps.** A period with no entries is itself a finding: either
   nothing was logged, or nobody was looking. Both are worth writing down.

See `reference.md` for the output format and a worked example.

## What not to do

Do not smooth a contradiction between two sources by picking the more
plausible one. Record both and mark the conflict — an unresolved disagreement
about ordering is frequently where the real finding is.
