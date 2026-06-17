# Prompt Engineering vs Loop Engineering

| | Prompt Engineering | [[Loop-Engineering]] |
|---|---|---|
| Unit of work | one crafted prompt | a self-driving loop |
| Who drives | you, every turn | the system, until done |
| Definition of done | you eyeball it | a machine-verifiable condition |
| Main failure | vague prompt | [[Goodharts-Law]] (gaming the verifier) |
| You write | the message | the goal + boundaries + verification |

Loop Engineering doesn't replace prompting — it wraps it. You still need a clear
instruction; you just also define when the loop stops and what it may not do.
(source: raw/articles/loop-engineering-source.md)

See also: [[Loop-Wiki-Map]]
