<div align="center">

# 🔁 obsidian-loop-wiki

**Turn your AI agent into a knowledge-base gardener that can't lie about its work.**

Most "let the AI organize my notes" setups quietly rot into AI-generated clutter.
`obsidian-loop-wiki` applies **Loop Engineering** to your Obsidian vault: every
ingest is a loop with a *machine-verifiable* definition of done — so the graph
actually grows, links actually connect, and nothing gets faked to pass.

Works with **Claude Code**, **Codex CLI**, **Gemini CLI**, or any agent that can
read an instructions file and run a Python script.

[Quickstart](#-quickstart) · [Why this exists](#-why-this-exists) · [How it works](#-how-it-works) · [中文说明](#-中文说明)

</div>

> _Add a demo GIF here: an Obsidian graph view starting empty, then exploding
> into a connected web as articles get ingested. This is the money shot — record
> it once your demo vault is open in Obsidian._

---

## ✨ Why this exists

The blog-post version of this idea is everywhere: *"point Claude at your Obsidian
vault and tell it to organize your notes."* It works for a week. Then:

- The agent invents a new folder scheme every session — `summary/`, then
  `notes/`, then `归档/`.
- Pages pile up but never link to each other. Open the graph view: a cloud of
  disconnected dots.
- You can't tell which claim came from a source and which the AI made up.
- Told to "make all checks pass," the agent deletes the failing note instead of
  fixing it. ([Goodhart's law](https://en.wikipedia.org/wiki/Goodhart%27s_law),
  but faster and with no guilt.)

`obsidian-loop-wiki` is the disciplined version. It treats each organizing pass
as a **loop** (in the [Loop Engineering](#-credits--source-material) sense) with
three things the blog versions lack:

1. **A machine-checkable goal** — `verify_wiki.py` fails the run if any node is
   an orphan, any `[[wikilink]]` is broken, or the audit log is stale.
2. **Guardrails** — `raw/` source material is read-only; inferences are flagged
   `待验证` (to-verify); the agent stops and asks when unsure instead of guessing.
3. **An anti-gaming rule** — the goal is a *trustworthy, connected graph*, never
   a green checkmark. Deleting content or sources to pass is explicitly forbidden.

That verifier is the moat. It's the difference between a vault you trust and a
pile of confident-sounding AI slop.

## 🚀 Quickstart

```bash
git clone https://github.com/uninhibited-scholar/obsidian-loop-wiki
cd obsidian-loop-wiki

# 1. See it work instantly on the bundled demo vault:
python3 scripts/verify_wiki.py demo-vault
#  → PASS — graph is connected, links resolve, audit trail current.

# 2. Open demo-vault/ in Obsidian (Open folder as vault) and look at the graph.
```

Point it at **your** vault by setting one environment variable:

```bash
export WIKI_PATH="$HOME/MyVault"   # macOS/Linux; WSL users: set inside WSL
```

Then install for your agent of choice:

| Agent | Install |
|-------|---------|
| **Claude Code** | `./install.sh` (copies the skill to `~/.claude/skills/loop-wiki/`) |
| **Codex CLI / Gemini CLI / others** | copy [`AGENTS.md`](AGENTS.md) into your project root |

Now just talk to your agent:

> *"收录这篇文章 raw/articles/xxx.md"* · *"整理 inbox"* · *"ingest this article"*
> · *"organize my vault and grow the graph"*

## 🧠 How it works

A vault is a set of **typed nodes** that link to each other, plus three control
files that keep the agent honest:

```
$WIKI_PATH/
├── SCHEMA.md       # the rulebook the agent obeys (naming, linking, trust)
├── index.md        # the entry map
├── log.md          # the audit trail — every change, dated, with its source
├── raw/            # source material — APPEND-ONLY, READ-ONLY
├── concepts/       # durable ideas (RAG, Loop Engineering …)
├── entities/       # tools, people, companies, projects
├── comparisons/    # "X vs Y" pages that grow over time
├── queries/        # answers worth keeping
├── moc/            # Maps of Content — reading routes, not file listings
└── drafts/         # outputs: articles, threads, scripts
```

The loop, every run:

```
source → agent splits into typed nodes → forces [[wikilinks]] → cites sources
   → flags unverified claims → updates index.md + log.md → verify_wiki.py
   → if FAIL, fix the real gap and retry → PASS
```

Human judges what's true. Agent compiles and links. Obsidian stores and
visualizes. The verifier makes the whole thing auditable.

## 📂 What's in here

| Path | What it is |
|------|------------|
| `skill/` | The Claude Code skill (`SKILL.md` + references + script) |
| `AGENTS.md` | Same workflow for Codex CLI / Gemini CLI / other agents |
| `scripts/verify_wiki.py` | Standalone verifier — no dependencies, just Python 3 |
| `templates/` | `SCHEMA.md` / `index.md` / `log.md` starters for a new vault |
| `demo-vault/` | A small, fully-linked vault you can open in Obsidian today |

## ❤️ Credits & source material

This packages a workflow that several people have been building in the open. The
ideas come from:

- **Loop Engineering** — the concept (designing loops to prompt agents instead of
  writing one-shot prompts) crystallized in mid-2026 by Peter (OpenClaw), Boris
  (Claude Code), and Addy Osmani's write-up.
- The **Obsidian + AI "second brain"** community — the typed-node + wikilink +
  SCHEMA/index/log discipline, and the "compile an article into a knowledge
  graph" framing.

`obsidian-loop-wiki` is an attempt to turn that scattered, do-it-yourself
practice into one mature, reusable, agent-agnostic tool. PRs and issues welcome.

## 📄 License

MIT — see [LICENSE](LICENSE).

---

## 🀄 中文说明

**让你的 AI agent 成为一个「不会对自己工作撒谎」的知识库园丁。**

市面上「让 AI 帮我整理 Obsidian 笔记」的玩法满天飞，但跑一周后都会烂成**一堆
AI 生成的垃圾**：agent 每次换一套文件夹命名、页面堆了一地却互不链接、分不清哪句
是原文哪句是 AI 编的、让它「让检查通过」它就直接把出错的笔记删了。

`obsidian-loop-wiki` 是这套思路的**纪律版**——把每一次整理当成一个
**Loop Engineering 的循环**，带上博主版本都没有的三样东西：

1. **可被机器验证的目标**：`verify_wiki.py` 会在出现孤儿节点、断链、日志过期时直接判定失败。
2. **边界护栏**：`raw/` 原始资料只读、推断内容标 `待验证`、拿不准就停下来问。
3. **防作弊铁律**：目标是「可信、互联的图谱」，绝不是一个绿勾——靠删内容/删来源凑过检查是明令禁止的。

这个 verifier 就是护城河：它决定了你的库是「可信的第二大脑」还是「一堆听起来很对的 AI 废话」。

**快速开始：**

```bash
git clone https://github.com/uninhibited-scholar/obsidian-loop-wiki
cd obsidian-loop-wiki
python3 scripts/verify_wiki.py demo-vault   # 先在样例库上看效果 → PASS
export WIKI_PATH="$HOME/MyVault"            # 指向你自己的库
./install.sh                                # Claude Code 用户；其他 agent 拷 AGENTS.md
```

然后直接对 agent 说：「收录这篇文章 raw/articles/xxx.md」「整理 inbox」即可。

支持 **Claude Code / Codex CLI / Gemini CLI**，或任何能读指令文件 + 跑 Python 的 agent。
欢迎 PR 和 issue。许可证 MIT。
