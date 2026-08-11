# QE_test-airia-skills-demo

Public test fixture for **Skills Over MCP** (SEP-2640) against the Airia MCP
Gateway. Served through mcp-link's skills mode as a `SkillLink` custom server.

## Skills

| Skill | Path | Exercises |
|---|---|---|
| `csv-insights` | `csv-insights/` | Supporting file read (`scripts/profile.py`) |
| `incident-timeline` | `incident-timeline/` | Second supporting file (`reference.md`) |
| `data-quality` | `analysis/data-quality/` | Nested category folder — layout-agnostic discovery |

## Why this shape

Each skill covers a distinct part of the gateway's read path:

- **Multiple skills** exercise catalog aggregation and per-source namespacing.
- **Supporting files** exercise Layer 2/3 reads — the host fetches `SKILL.md`
  first, then follows references on demand. There is no bundle fetch; every
  file is its own `resources/read`.
- **The nested skill** confirms discovery does not assume a flat root layout.

## Conventions the converter enforces

- The folder name must equal `frontmatter.name`. `csv-insights/SKILL.md`
  requires `name: csv-insights`.
- Entries are published under the `skill://` scheme. The gateway drops any
  other scheme by design in v1.
- The `description` is what a host sees at discovery time and is the only
  thing it uses to decide relevance. The body loads only after that decision,
  so descriptions should say *when to reach for this*, not just what it does.

## Testing against a gateway

Preview the catalog before registering the server:

```bash
curl -sS -X POST "$GATEWAY/api/custom-remote-servers/test-skills" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"repoUrl":"https://github.com/krp-airia/QE_test-airia-skills-demo"}'
```

Expect `ok: true` with a `skillCount` of 3.
