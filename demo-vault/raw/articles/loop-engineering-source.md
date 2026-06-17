# Source: The rise of Loop Engineering (2026)

> raw source note — append-only, do not edit. This is the evidence layer.

In mid-2026 a new term started circulating: **Loop Engineering**. The claim, from
practitioners building coding agents, was that you no longer write one-shot
prompts for an agent — you design the *loop* that prompts the agent for you.

A complete loop was described as having five parts: a heartbeat (cron / interval
/ hooks), worktree isolation for parallel agents, a project knowledge system
(not just one skill), connectors (MCP) to reach real tools, and a separate
sub-agent that verifies the work.

The soul of it, the authors stressed, is **defining a goal a machine can
verify** — "all tests pass, zero lint errors" beats "make it better." The classic
trap is Goodhart's law: once a metric becomes the target, the agent optimizes the
metric, not your intent — e.g. deleting failing tests to make the suite pass.

In parallel, the Obsidian + AI community had been building "second brain" vaults
where an agent compiles articles into typed, wikilinked nodes that form a visible
knowledge graph. This vault is the meeting point of the two ideas.
