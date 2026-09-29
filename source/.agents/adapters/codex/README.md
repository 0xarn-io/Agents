# OpenAI Codex and GPT API notes

Sources: `.agents/SOURCES.md` [S2], [S14]-[S16], checked 2026-09-28, and a review by GPT-6
Astra in Codex CLI 0.153.4 on 2026-09-29. Confirm loading and invocation on your version with
`tests/BEHAVIORAL_EVALS.md`.

## Loading

Codex reads `AGENTS.md` (or `AGENTS.override.md`) from `~/.codex`, then from the project
root down to the working directory, concatenating them up to `project_doc_max_bytes`
(32 KiB by default). The root `AGENTS.md` here is a small loader well under that limit; the
shared files it points to are read on demand. Codex does not read `CLAUDE.md`. Skills in
`.agents/skills/` are discovered natively, and each skill's `agents/openai.yaml` keeps it
opt-in (`allow_implicit_invocation: false`).

## Models (September 2026)

Values below come from OpenAI's documentation and differ by plan and Codex version. Use only
the model IDs and effort values your installed host exposes; otherwise inherit the current
model. In the 2026-09-29 review session, Astra's delegation interface also exposed `xhigh`,
`max`, and `ultra`, and Sol/Luna were not offered as delegate overrides.

| Model | Use |
|---|---|
| `gpt-6-astra` | Flagship: hardest coding and multi-step work. Documented effort `low`/`medium`/`high` (no `none`); newer hosts may expose more. |
| `gpt-6-sol` | Strong reasoning at mid-tier cost; Codex's default for demanding subagent work. Effort `none`-`high`. |
| `gpt-6-luna` | Fast and cheap; Codex's default for narrow subagent work. Effort `none`-`high`. |
| GPT-5.5 / 5.4 / 5.3-Codex, 5.4-mini/nano | Previous generation. mini/nano follow instructions literally: use only for narrow, fully specified tasks. |

## Routing delegated work

Codex custom agents in `.codex/agents/*.toml` can pin `model` and `model_reasoning_effort`;
the file value takes precedence over Codex defaults. The files in `agents/` here mirror this
project's quality-first routing (the Claude equivalent is
`adapters/claude-code/MODEL-ROUTING.md`). Copy them into `.codex/agents/` to use them:

| Agent file | Model, effort | Use |
|---|---|---|
| `explorer.toml` | `gpt-6-luna`, `medium`, read-only | Mechanical lookups and bulk read-only sweeps |
| `implementer.toml` | `gpt-6-sol`, `high` | Planned implementation tasks |
| `reviewer.toml` | `gpt-6-astra`, `high`, read-only | Independent task and branch reviews; anything safety-relevant |

If your plan does not offer a model named in these files, change it to one `/model` lists
(for example the reviewer to `gpt-6-sol` at `high`, or the explorer and implementer to
`gpt-6-astra` when Sol/Luna are not available). Safety-relevant work still needs the qualified human review in `AGENT_RULES.md`.
`agents.max_concurrent_threads_per_session` under `[agents]` in `config.toml` caps
concurrency; `agents.default_subagent_model` sets the fallback model. `agents.enabled = false`
removes the collaboration tools entirely; in Codex CLI 0.153.4, `--disable multi_agent` did
not. The JSON event stream logs subagent work only as `collab_tool_call` items, often a `wait`
without the spawn, so read the agent messages to see what was delegated.

## Windows: Python inside the sandbox

Codex's Windows sandbox cannot read a Python installed per user (under
`%LOCALAPPDATA%\Programs\Python`), so `python` is "not recognized" and the agent cannot run
tests. It reports that honestly, but the check does not happen. Either install Python for all
users, or put a readable interpreter on the sandbox's PATH, such as the runtime Codex ships:

```toml
# ~/.codex/config.toml; adjust the runtime path to what exists on your machine
[shell_environment_policy.set]
PATH = 'C:\Users\<you>\.cache\codex-runtimes\codex-primary-runtime\dependencies\python;C:\Windows\System32;C:\Windows;C:\Windows\System32\WindowsPowerShell\v1.0;C:\Program Files\Git\cmd'
```

With that setting, GPT-6 Astra ran the eval fixture's tests inside the sandbox (2026-09-29).

## Prompting notes

- Contradictions hurt: GPT-5 and later spend reasoning trying to reconcile conflicting
  instructions. The bundle's precedence order in `AGENT_RULES.md` exists for this; keep new
  project rules consistent with it rather than adding overrides in several places.
- GPT-6 Astra weighs skill files heavily; the baseline states that the user's direct
  instruction wins over a skill's guidance within safety and permission limits.
- Persistence: the models are trained to keep going until the task is complete, which
  matches "Progress updates and ending a turn". For Codex models, keep the one-line intent
  and skip long upfront plan messages; record the plan as a checklist instead.
- Remove `temperature`, `top_p`, and `top_logprobs` when reasoning is not `none`. Start at
  `medium` effort; OpenAI notes that clearer prompts and output contracts usually recover
  more quality than raising effort.
- Prefer `rg` for searching and the host's file tools over shell edits when both exist.
