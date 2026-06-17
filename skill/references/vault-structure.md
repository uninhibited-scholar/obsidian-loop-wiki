# Vault structure

A loop-wiki vault is shared by two consumers: **Obsidian** (visualizes the graph
and backlinks) and the **Agent** (reads, writes, and links pages). They must
point at the *same* folder, which is `WIKI_PATH`.

```
$WIKI_PATH/
├── SCHEMA.md          # the rulebook — the Agent obeys this
├── index.md           # the entry map — links to key nodes & MOCs
├── log.md             # the audit trail — every change, dated, with source
├── raw/               # source material; append-only, read-only
│   ├── articles/
│   ├── papers/
│   ├── transcripts/
│   └── assets/
├── concepts/          # durable ideas that recur across sources
├── entities/          # tools, people, companies, projects
├── comparisons/       # "X vs Y" pages that accrete over time
├── queries/           # answers worth keeping long-term
├── moc/               # Maps of Content (reading routes, not listings)
└── drafts/            # outputs: articles, threads, scripts
```

## Why this shape

- **One type per folder.** If every page is the same kind of thing, wikilinks
  carry no structure — you get a hairball, not a graph. Separating concepts from
  entities keeps terms from blurring into proper nouns.
- **`raw/` is the evidence layer.** Conclusions elsewhere cite back into `raw/`.
  If the Agent could rewrite originals, the whole chain of trust collapses — so
  `raw/` is append-only and read-only.
- **`moc/` is a route, not a directory.** Its job is "read this, then this,"
  which is what turns a collection into understanding.
- **`drafts/` is the point.** A knowledge base that never outputs anything is
  just a fancier hoard.

## Setup notes

- Open in Obsidian with **Open folder as vault**, selecting the whole vault root
  — never a subfolder like `raw/`. Both Obsidian and the Agent need the full
  tree.
- Set `WIKI_PATH` in the same environment the Agent runs in. On macOS/Linux:
  `export WIKI_PATH="$HOME/MyVault"`. On Windows + WSL, set it inside WSL with a
  `/mnt/c/...` path, not in PowerShell — a mismatch here is the classic "why
  isn't Obsidian changing?" bug.
- Verify the link is live: `echo "$WIKI_PATH" && ls "$WIKI_PATH"` should list
  the control files and folders above.

## Variants

Some users prefer a leaner `Inbox/ + Wiki/ + Output/` layout (new material lands
in `Inbox/`, gets compiled into `Wiki/` with its own `Index.md`/`Log.md`,
finished work goes to `Output/`). That's the same three-layer idea —
input / processing / output — with fewer node types. If a vault already uses it,
follow its `SCHEMA.md`; don't impose the folders above on top of it.
