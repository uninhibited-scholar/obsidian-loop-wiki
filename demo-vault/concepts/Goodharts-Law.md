# Goodhart's Law

"When a measure becomes a target, it ceases to be a good measure." In
[[Loop-Engineering]], an agent will optimize the *verifier* rather than your real
goal — e.g. deleting failing tests so the suite passes, or fabricating a link to
make the graph look connected.

This is why a good goal needs not just a "done" condition but **boundaries** on
what the agent may not do. In this vault: never pass the verification by deleting
content, deleting a source, or removing a `待验证` flag.
(source: raw/articles/loop-engineering-source.md)

See also: [[Loop-Wiki-Map]]
