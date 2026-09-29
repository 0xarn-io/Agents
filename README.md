# Agents

One set of engineering rules and two opt-in skills for AI coding agents. It works in
**Claude Code** (Claude Opus 5.5, Sonnet 5.5), **Codex** (GPT-6 Astra, Sol, Luna), and
**Grok Build** (Grok 4.7) without keeping three copies. The rules are shared, and each host
gets a small adapter for how it loads files and picks models.

## What's inside

```
source/                          ← copy the contents of this folder into your project root
├── AGENTS.md                    loader for Codex, Grok Build, and other AGENTS.md hosts
├── CLAUDE.md                    loader for Claude Code (@-imports the shared files)
└── .agents/
    ├── AGENT_RULES.md           the baseline every agent follows
    ├── CAPABILITIES.md          tool fallbacks, delegation, and model-selection rules
    ├── ARCHITECTURE.md          template: fill in your project's commands and constraints
    ├── AGENT_CONTEXT.md         generated single-file export for chat-only hosts
    ├── skills/
    │   ├── think-like-fable/    opt-in: deeper reasoning and verification habits
    │   └── super-code/          opt-in: design → plan → implement → review workflow
    ├── adapters/
    │   ├── claude-code/         model routing (haiku/sonnet/opus), per-model notes, wrappers
    │   ├── codex/               GPT-6 notes and custom-agent .toml files
    │   └── grok-build/          Grok notes and skill wrappers
    ├── tools/                   optional Python helpers (context export, plan task briefs)
    └── tests/                   contract and helper tests, behavioral eval cases
```

## Install into a project

1. Copy `source/AGENTS.md`, `source/CLAUDE.md`, and `source/.agents/` to your repository
   root. If the project already has an `AGENTS.md` or `CLAUDE.md`, merge them rather than overwrite.
2. Fill in `.agents/ARCHITECTURE.md` with the project's real build and test commands.
   On Windows, keep the project path under about 150 characters or enable Git long paths
   (`git config core.longpaths true`): the deepest bundle path is 101 characters.
3. Add the adapter for each host you use:

| Host | Loads automatically | Extra step |
|---|---|---|
| Claude Code | `CLAUDE.md`, which imports the rules and Claude model routing | Optional: copy `adapters/claude-code/<skill>/SKILL.md` to `.claude/skills/<skill>/` for slash commands |
| Codex | `AGENTS.md`, and the skills in `.agents/skills/` (kept opt-in by `agents/openai.yaml`) | Optional: copy `adapters/codex/agents/*.toml` to `.codex/agents/` for routed subagents |
| Grok Build | `AGENTS.md` and `CLAUDE.md`, and the skills in `.agents/skills/` | **Recommended:** copy `adapters/grok-build/<skill>/SKILL.md` to `.grok/skills/<skill>/` so the skills stay opt-in |
| Chat-only / API | Nothing | Paste or attach `.agents/AGENT_CONTEXT.md` |

Full loading details, including other hosts: [`source/.agents/README.md`](source/.agents/README.md).

## Using the skills

Both skills are off until you ask for them by name:

> Use think-like-fable for this task.
> Use super-code for this task.

A normal request such as "fix this bug" runs on the baseline rules alone. Those rules still
cover exploring before editing, keeping changes small, running a real check before calling
work done, and not committing or pushing unless you ask.

## Tests

From `source/`:

```bash
python -m unittest discover -s .agents/tests -p "test_*.py" -v
```

62 tests (1 skipped on Windows) passed on 2026-09-29 on Windows 11 with Python 3.14. After
editing `AGENT_RULES.md`, `skills/SKILLS.md`, or `CAPABILITIES.md`, regenerate the export:

```bash
python .agents/tools/export_context.py --output .agents/AGENT_CONTEXT.md
```

CI runs the tests on Linux, Windows, and macOS (Python 3.9 and 3.13) for every push and pull
request, and fails if `AGENT_CONTEXT.md` is stale.

## Releases

Each [release](https://github.com/0xarn-io/Agents/releases) has
`agents-bundle-<version>.zip`, which holds the contents of `source/` ready to unzip into a
project root, plus a SHA-256 checksum. To publish a new one, add a `# Revision:` entry to
`source/.agents/CHANGELOG.md`, then:

```bash
git tag v2026.09.29 && git push origin v2026.09.29
```

The release workflow runs the full test matrix first and publishes only if it passes.

## Review status

On 2026-09-29, Claude Opus 5.5 (Claude Code), Grok 4.7 (Grok Build), and GPT-6 Astra (Codex)
each reviewed the bundle read-only in their own host. They went through four rounds and all
three signed off "good for all". The rounds are recorded in
[`VALIDATION.md`](source/.agents/VALIDATION.md).

The same day, [`evals/`](evals/README.md) ran 7 behavioral cases headless in each tool, on
Claude Opus 5.5, Sonnet 5.5, GPT-6 Astra, and Grok 4.7. Each run used a throwaway repository
with a real bug, a dirty working tree, and a log containing an injected instruction. 26 of 28
runs passed. The other two acted on nothing but didn't report the injected instruction. After
a one-line rule fix, 8 of 8 re-runs reported it. Re-run the evals with
`python evals/run_evals.py`.

