# Grok Build and Grok API notes

Sources: `.agents/SOURCES.md` [S17]-[S20], checked 2026-09-28, and a review by Grok 4.7
in Grok Build 1.0.44 on 2026-09-29 (its installed user guide and tool schema). Confirm on
your version with `grok inspect` and `tests/BEHAVIORAL_EVALS.md`.

## Loading

Grok Build reads project rules from `AGENTS.md` and also from `CLAUDE.md` (plus
`.grok/rules/*.md`, `.claude/rules/`, `.cursor/rules/`), walking from the repository root down
to the working directory, with no size cap. In this repository it therefore loads both root
loaders. That is harmless: Grok Build does not expand `@` imports, so `CLAUDE.md` is read as
a list of pointers to the same shared files, and root `AGENTS.md` directs it to open them. The `MODEL-ROUTING.md` pointer applies only to
Claude hosts; Grok follows the notes below. Run `grok inspect` to see what was found.

Grok Build also discovers skills in the project's `.agents/skills/` (as well as
`.grok/skills/` and the user-level skill folders), so both shared skills are listed in every
session. The shared `SKILL.md` files stay vendor-neutral and carry no invocation flag, which
leaves only the prose policy between a description match and an unrequested workflow.
**Install the wrappers** so the opt-in is enforced by the host: a `.grok/skills/` skill takes
priority over the same name in `.agents/skills/`, and the wrappers set
`disable-model-invocation: true`:

```sh
mkdir -p .grok/skills/think-like-fable .grok/skills/super-code
cp .agents/adapters/grok-build/think-like-fable/SKILL.md .grok/skills/think-like-fable/
cp .agents/adapters/grok-build/super-code/SKILL.md .grok/skills/super-code/
```

The wrappers delegate to the shared source. Merge rather than overwrite existing skills.

## Models

`grok-4.7` is the flagship for code and agentic tool calling, with reasoning effort `low`,
`medium`, `high`, or `xhigh` (see [S20] for context size and dated snapshots). `grok models`
lists what your account can use; Grok Build 1.0.44 offered `grok-4.7`, `grok-4.7-build-fast`,
`grok-4.6`, and `grok-4.5`.

**This table is user configuration, not something the agent passes.** The model-facing
`spawn_subagent` tool has no `effort` or `subagent_type` argument. It has a `model` argument
unless subagent model inheritance is turned on; pass one only when the schema lists it, and
only an ID from `grok models`. Otherwise delegates inherit what the user configured. Set it with
`/effort` or `--effort` for the session, and optionally `[subagents.models]` in the Grok
Build config to override the model per subagent type; without an override, a subagent
inherits the parent's model.

| Task | Suggested user setting |
|---|---|
| Mechanical, lookup, bulk read-only | `low` effort, or a lighter model for `explore` via `[subagents.models]` |
| Small, well-specified change | `medium` |
| Medium to hard work, reviews | `high` |
| Hardest work, safety-relevant review | `xhigh`, plus the qualified human review in `AGENT_RULES.md` |

Custom subagents live in `.grok/agents/`; no agent files are shipped here because the
per-agent fields are not publicly documented. Check `/agents` in your installed version.

## Prompting notes

- Give detailed, structured context: xAI recommends thorough system prompts with explicit
  goals and edge cases, sectioned with Markdown headings or XML tags. The shared bundle
  already works this way.
- Name the specific files a task concerns; vague requests ("make error handling better")
  drift.
- Use native tool calling, not tool calls written as XML text.
- API apps: keep the conversation history append-only and pass encrypted reasoning back
  unchanged; set `prompt_cache_key` (Responses API) or the `x-grok-conv-id` header (Chat
  Completions) so requests hit a warm cache; use context compaction for long agent loops.
