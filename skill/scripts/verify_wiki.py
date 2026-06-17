#!/usr/bin/env python3
"""Verify a loop-wiki vault against the machine-checkable completion criteria.

Usage: python3 verify_wiki.py [VAULT_PATH]
(falls back to the WIKI_PATH environment variable if no arg is given)

Exit code 0 = all criteria pass; 1 = something needs fixing; 2 = bad invocation.

This is the Loop Engineering "definition of done": orphan nodes, broken
wikilinks, and a stale audit trail are exactly the silent failures that turn an
AI-maintained vault into clutter. The checker reports them; it never fixes them
by deleting things — that would be gaming the goal, which is the one failure
mode this whole skill exists to prevent.
"""
import os
import re
import sys

# Node folders whose pages are expected to participate in the graph.
NODE_DIRS = ["concepts", "entities", "comparisons", "queries", "moc"]
CONTROL = ["SCHEMA.md", "index.md", "log.md"]
WIKILINK = re.compile(r"\[\[([^\]|#]+)")  # captures target, ignores |alias and #heading
TOVERIFY = re.compile(r"待验证|to-?verify", re.IGNORECASE)


def md_files(root):
    for dirpath, _, names in os.walk(root):
        for n in names:
            if n.endswith(".md"):
                yield os.path.join(dirpath, n)


def main():
    vault = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("WIKI_PATH", "")
    if not vault:
        print("ERROR: no vault path given and WIKI_PATH is unset.")
        return 2
    vault = os.path.expanduser(vault)
    if not os.path.isdir(vault):
        print(f"ERROR: not a directory: {vault}")
        return 2

    problems = []
    notes = []

    # Map basename (without .md) -> path, for resolving wikilinks.
    by_stem = {}
    for f in md_files(vault):
        by_stem.setdefault(os.path.splitext(os.path.basename(f))[0], f)

    # 1) Orphan nodes: a node page with zero outgoing wikilinks.
    newest_node_mtime = 0.0
    toverify_count = 0
    for d in NODE_DIRS:
        ddir = os.path.join(vault, d)
        if not os.path.isdir(ddir):
            continue
        for f in md_files(ddir):
            text = open(f, encoding="utf-8", errors="ignore").read()
            links = WIKILINK.findall(text)
            if not links:
                problems.append(f"ORPHAN: {os.path.relpath(f, vault)} has no [[wikilinks]]")
            toverify_count += len(TOVERIFY.findall(text))
            newest_node_mtime = max(newest_node_mtime, os.path.getmtime(f))

    # 2) Broken wikilinks: a [[target]] that resolves to no file.
    for f in md_files(vault):
        if os.path.basename(f) in CONTROL:
            continue
        text = open(f, encoding="utf-8", errors="ignore").read()
        for target in WIKILINK.findall(text):
            stem = target.strip()
            if stem and stem not in by_stem:
                problems.append(
                    f"BROKEN LINK: {os.path.relpath(f, vault)} -> [[{stem}]] resolves to nothing"
                )

    # 3) Control files present.
    for c in CONTROL:
        if not os.path.isfile(os.path.join(vault, c)):
            problems.append(f"MISSING: {c} (run the Initialize a vault flow)")

    # 4) Audit trail freshness: if nodes were touched more recently than the log
    #    or index, the run probably forgot to record itself.
    for c in ("log.md", "index.md"):
        p = os.path.join(vault, c)
        if os.path.isfile(p) and newest_node_mtime > os.path.getmtime(p) + 1:
            problems.append(
                f"STALE: {c} is older than the newest node — did this run update it?"
            )

    if toverify_count:
        notes.append(f"{toverify_count} item(s) flagged 待验证 (to-verify) — good, keep them marked.")

    print(f"loop-wiki verification — vault: {vault}\n")
    for n in notes:
        print(f"  note: {n}")
    if not problems:
        print("\nPASS — graph is connected, links resolve, audit trail current.")
        return 0
    print(f"\nFAIL — {len(problems)} issue(s):")
    for p in problems:
        print(f"  - {p}")
    print(
        "\nFix the real gap (add the missing link, update log.md/index.md). "
        "Do NOT pass by deleting content, sources, or to-verify flags."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
