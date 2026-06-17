# AGENTS.md — obsidian-loop-wiki

> Drop this file in your project root so Codex CLI, Gemini CLI, or any
> agent that reads an instructions file follows the same loop as the Claude Code
> skill. (Claude Code users: run `./install.sh` instead — it installs the richer
> skill version.)

You maintain an Obsidian knowledge base as a **verifiable loop**. Raw material
goes in; you compile it into typed, cross-linked nodes that form a graph, and
every run leaves an audit trail. The point of the discipline below is that an
agent told to "just organize my notes" produces AI-generated clutter — drifting
names, orphan pages, unsourced claims. The loop prevents that.

## Locate the vault first

The vault path is in the `WIKI_PATH` environment variable. Never guess it.

```bash
echo "$WIKI_PATH" && ls "$WIKI_PATH"
```

If `WIKI_PATH` is unset, ask the user for their vault path. If the path has no
`SCHEMA.md`, it's uninitialized — scaffold it from `templates/` before doing
anything. Otherwise read `SCHEMA.md`, `index.md`, `log.md` first; `SCHEMA.md`'s
rules override your instincts.

## Node types (keep separated)

- `raw/` — sources. **Append-only, read-only. Never edit originals.**
- `concepts/` — durable ideas recurring across sources.
- `entities/` — tools, people, companies, projects.
- `comparisons/` — "X vs Y" pages that accrete over time.
- `queries/` — answers worth keeping.
- `moc/` — Maps of Content (reading routes, not listings).
- `drafts/` — outputs.

## Ingest an article / organize the inbox

1. Read the source; extract core themes. Do not modify originals.
2. Create/update the right typed nodes per `SCHEMA.md`.
3. **Cross-link with `[[wikilinks]]`** — every new node links to ≥1 existing
   node. An orphan node is a failed run. This single rule is what makes a graph
   exist instead of a pile of islands.
4. Cite sources: `(source: raw/articles/<file>.md)`.
5. Flag inferences/unconfirmed claims as `待验证` (to-verify). Never launder a
   guess as fact.
6. Update `index.md` (notable nodes) and the relevant `moc/` map.
7. Append a dated `log.md` entry: source, files created/updated, to-verify items.
8. Run the verification pass below and report exactly what you created/updated.
   If unsure where something belongs, stop and ask — a wrong classification
   pollutes the graph silently.

## Verification pass (definition of done)

```bash
python3 scripts/verify_wiki.py "$WIKI_PATH"
```

It checks: no orphan nodes, no broken wikilinks, `index.md`/`log.md` updated this
run, to-verify items still marked.

**Do not game the verifier.** The goal is a trustworthy, connected graph — not a
green checkmark. Never pass by deleting content, deleting a failing source,
removing a to-verify flag, or inventing a link to an unrelated node. If it can't
pass honestly, report what's wrong and let the user decide. If it fails, fix the
*real* gap (add the missing link, update the log) and rerun. That retry-until-
honestly-green behavior is the loop.
