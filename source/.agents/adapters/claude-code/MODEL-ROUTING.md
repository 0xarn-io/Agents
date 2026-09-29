# Model routing for delegated work (Claude hosts)

Owner preference for this project, for Claude hosts only (Claude Code, Claude Agent SDK);
Codex and Grok Build have their own notes in `.agents/adapters/`. It applies whenever the host lets you choose a model per
subagent or task (a `model` argument on a subagent/Agent tool, an orchestration mode, or an
SDK option). Without that capability, use the current model and ignore this file; never
invent a model identifier or selector argument.

Pick the smallest model that will do the task well, and set the model explicitly on every
dispatch: an omitted model usually inherits the session's (most expensive) model.

| Task | Model alias | Examples |
|---|---|---|
| Mechanical, lookup, or bulk read-only work | `haiku` | find files/symbols, collect grep results, summarize logs, rename across files from an exact list, format/convert data |
| Small, well-specified change or check | `sonnet` | one-function fix with a known cause, add a focused test, apply a written plan step touching 1-2 files |
| Medium to hard work | `opus` | multi-file features, refactors, root-cause debugging, design choices, reviewing risky or safety-relevant changes, final whole-branch review, PLC/TwinCAT logic |

- The `sonnet` alias resolves to the host's current Sonnet (Sonnet 5.5 where available).
  Run Sonnet delegates at `high` effort (its default) when the host lets you set effort per
  delegate; at `low`/`medium` it may stop early or skip real checks. Every Sonnet or Haiku
  brief states the check that proves the task done.
- Do not route work to `fable`. The owner has excluded it, including for creative work.
- The controller (the session holding the plan and talking to the user) stays on its current
  model; routing applies to delegates.
- Write briefs for `haiku` and `sonnet` as complete, literal instructions: they follow the
  words closely and do not fill gaps the way a larger model does. State scope explicitly
  ("every endpoint in `routes/`, not only the first").
- Escalate one tier (haiku → sonnet → opus) when a delegate reports BLOCKED or NEEDS_CONTEXT
  for reasoning reasons, returns work that fails review twice, or the task turns out larger
  than briefed. Do not retry the same model with the same brief.
- The owner puts quality before speed. Independent reviewers are welcome: use them for every
  `super-code` task review and for any risky or safety-relevant change, on `opus`. Skip
  delegation only where it adds nothing, such as a lookup that one search answers.
- Safety-critical work (machine safety functions, interlocks, safe states) is never routed
  below `opus`, and still needs the qualified human review required in `AGENT_RULES.md`.
