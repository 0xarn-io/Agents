# Grok Build and Grok API notes

Sources: `.agents/SOURCES.md` [S17]-[S20], checked 2026-09-28, and a review by Grok 4.7
in Grok Build 1.0.44 on 2026-09-29 (its installed user guide and tool schema). Confirm on
your version with `grok inspect` and `tests/BEHAVIORAL_EVALS.md`.

## Loading

Grok Build loads a project's `AGENTS.md`, `CLAUDE.md`, project skills, and `.grok/config.toml`
only after the folder is trusted: accept the trust prompt on first launch, or run
`/hooks-trust`. Until then none of this bundle applies. The grant is stored in
`~/.grok/trusted_folders.toml`. `grok inspect` shows what loaded.

Grok Build reads project rules from `AGENTS.md` and also from `CLAUDE.md` (plus
`.grok/rules/*.md`, `.claude/rules/`, `.cursor/rules/`), walking from the repository root down
to the working directory, with no size cap. In this repository it therefore loads both root
loaders. That is harmless: Grok Build does not expand `@` imports, so `CLAUDE.md` is read as
a list of pointers to the same shared files, and root `AGENTS.md` directs it to open them. The `MODEL-ROUTING.md` pointer applies only to
Claude hosts; Grok follows the notes below. Run `grok inspect` to see what was found.

Grok Build also discovers skills in the project's `.agents/skills/` (as well as
`.grok/skills/` and the user-level skill folders), so both shared skills are listed in every
session. The shared `SKILL.md` files stay vendor-neutral and carry no invocation flag. The
bundle therefore ships Grok wrappers at the repository root in `.grok/skills/<name>/SKILL.md`:
they take priority over the same names in `.agents/skills/`, set
`disable-model-invocation: true`, and delegate to the shared source. Installing the bundle
installs them. If the project already has a `.grok/skills/` folder, merge rather than
overwrite. Check with `grok inspect`.

## Built-in skills and git actions

Grok Build ships bundled skills. Its `execute-plan` triggers on requests like "execute the
plan" and runs subagents in worktrees, commits, builds a branch stack, and pushes. In evals
it did so even after reading `AGENT_RULES.md`. The bundle handles this in two layers:

- `.grok/skills/execute-plan/SKILL.md` overrides the bundled skill (a project skill with the
  same name wins). It executes the plan in the current working tree under the shared rules,
  with no branches, worktrees, commits, or pushes unless the user asks. To get Grok's
  branch-stack workflow back in a project, delete that folder.
- `.grok/config.toml` adds `ask` rules for commit, push, merge, rebase, hard reset, stash, checkout, restore, clean, worktree
  creation, and PR submission. In `auto` mode they make Grok ask before those commands;
  without them the auto classifier allowed a commit. Grok Build 1.0.44 skips `ask` rules
  under `--always-approve`/`bypassPermissions`, and they cannot stop the host itself from
  creating subagent worktrees, which is why the skill override exists.

A project `.grok/config.toml` can only set `[mcp_servers]`, `[plugins]`, and `[permission]`.
To stop any other bundled skill from triggering, add it to `[skills] disabled` in your own
`~/.grok/config.toml`. Merge with an existing project `.grok/` folder rather than overwrite.

## Headless runs

In `grok -p` with `--permission-mode dontAsk` (or plan mode), a shell command that matches no
`--allow` rule cancels the whole session (`stop_reason: cancelled`), not just that call, so
the final report is lost. For unattended runs, allow every command the task needs, for
example `--allow 'Bash(python *)'`, or give exact file paths so the agent can use `read_file`
instead of the shell. An agent that cannot run a check should report the check it skipped
(see "Verification and reporting" in `AGENT_RULES.md`).

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
