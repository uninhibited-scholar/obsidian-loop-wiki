# Knowledge Base Schema

This file defines the rules for this vault. The agent must obey these rules on
every run. When a needed rule is missing, propose adding it here — do not
improvise silently.

## Folders
- `raw/`         Source material. APPEND-ONLY and READ-ONLY. Never edit originals.
- `concepts/`    Durable ideas that recur across sources.
- `entities/`    Tools, people, companies, projects. Kept separate from concepts.
- `comparisons/` "X vs Y" pages; accrete new dimensions as sources arrive.
- `queries/`     Answers worth keeping long-term.
- `moc/`         Maps of Content — reading routes, not file listings.
- `drafts/`      Outputs: articles, threads, scripts.

## Linking
- Important concepts MUST be written as `[[wikilinks]]`. No links → no graph.
- Every new node links to at least one existing node. Orphans are failures.
- Key conclusions cite their source: `(source: raw/articles/<file>.md)`.

## Trust
- Inferences and unconfirmed claims MUST be marked `待验证` (to-verify).
- Never satisfy a check by deleting content, sources, or to-verify flags, or by
  inventing a link to an unrelated node.

## Bookkeeping
- After any important change, append a dated entry to `log.md`.
- After adding a notable node, update `index.md`.

## Naming (tune to taste; keep it STABLE once chosen)
- Files are Markdown. Pick one naming convention and never drift from it.
- Example: `English-中文` folder names joined by a hyphen (e.g. `Tools-工具`);
  pure product names stay as-is (e.g. `Obsidian`); no numeric prefixes except
  top-level folders.
