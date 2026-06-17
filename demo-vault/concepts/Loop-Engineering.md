# Loop Engineering

Designing a **loop** that prompts an agent toward a goal, instead of hand-writing
one-shot prompts. You define the goal, the verification condition, and the
failure handling — then let the system run.

A complete loop has five parts: a heartbeat, worktree isolation, a project
knowledge system, connectors, and a verifying sub-agent.
(source: raw/articles/loop-engineering-source.md)

The soul of it is a goal a machine can verify — which is exactly what the
[[Knowledge-Graph]] verification pass provides for a vault. Its sharpest failure
mode is [[Goodharts-Law]]. Tools like [[Claude-Code]] productize the micro
version via a `/goal` command.

See also: [[Prompt-vs-Loop-Engineering]] · [[Loop-Wiki-Map]]
