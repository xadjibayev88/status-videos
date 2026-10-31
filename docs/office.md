# Org chart

19 agents in 6 teams around the Brain, led by the chief of staff (the Claude Code session itself, with its instructions in `CLAUDE.md`). Each worker is a file in `.claude/agents/`; 14 agents with no work for this business are kept in `.claude/agents-archive/`.

| # | Agent | Team | Job |
|---|---|---|---|
| lead | chief of staff | The Brain | Routes work, runs teams in parallel, reviews, reports (`CLAUDE.md`) |
| 1 | `research-director` | Research | Splits a question three ways, merges into one brief |
| 2 | `market-analyst` | Research | Market size, customers, pricing benchmarks |
| 3 | `competitor-analyst` | Research | Competitor profiles and the gap we can own |
| 4 | `trend-scout` | Research | What changed in the last 30 to 90 days |
| 5 | `script-writer` | Scripts | Short-form video scripts: hook, three beats, close; runs the Scripts team |
| 6 | `hook-writer` | Scripts | Ten ranked opening lines for any piece |
| 7 | `seo-specialist` | Scripts | Keywords, titles, descriptions, outlines |
| 8 | `fact-checker` | Scripts | Checks every claim in facts content against sources; PASS or FIX |
| 9 | `brand-checker` | Scripts | Reviews every creative deliverable against the brand rules; PASS or FIX |
| 10 | `engineering-lead` | Dev | Spec, delegates to devs, runs QA and review |
| 11 | `backend-dev` | Dev | Server, API, data and tooling code |
| 12 | `qa-tester` | Dev | Tests per acceptance criterion, reproduces bugs |
| 13 | `code-reviewer` | Dev | Ranked findings on the diff; PASS or FIX |
| 14 | `social-media-manager` | Social | Posts and calendar; runs the Social team |
| 15 | `community-manager` | Social | Replies to comments and DMs, flags what needs the owner |
| 16 | `analytics-lead` | Analytics | The weekly report: what the numbers mean, what to change |
| 17 | `data-analyst` | Analytics | Cleans exports, computes metrics and trends, shows the work |
| 18 | `strategist` | Analytics | Goal to options, recommendation, first three steps |

## How a request moves

```
owner  ->  chief of staff (the Brain)  ->  team head  ->  workers (parallel)
                 ^                              |               |
                 |                              v               v
              report  <----------  review (brand-checker / code-reviewer / head)
```

## The shared brain

`.mcp.json` starts the memory MCP server with its file at `brain/memory.jsonl`. Two entities: **Company** and **Brand rules**. Every agent reads them before working. When the owner says "from now on…", the chief of staff writes it there, so every agent remembers it on the next run. Edit the JSONL by hand to seed it.

## The 3D office

`office/index.html` draws this chart as a 3D floor: the Brain in the middle, one room per team around it, one desk and character per agent, heads wear a hat. The top bar has Office, Tasks (the live log) and Brain (the memory file) tabs, the running counter, and the model chips; the minimap sits bottom right. `office/build.py` turns the table in `CLAUDE.md` plus the agent files into `office/agents.json`; `office/serve.py` serves the page, streams `office/events.jsonl` (written by the hooks in `.claude/settings.json` on every sub-agent start and stop) and exposes the brain at `/brain`.

## Adding an agent

`/hire <name>: <job>` writes the file and updates this chart. Keep one job per agent, say when to use it in the description (that is how the chief of staff picks it), and give it only the tools it needs.
