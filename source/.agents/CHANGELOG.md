# Revision: three-model review (Claude, Grok, GPT) — 2026-09-29

- Baseline: exploration scales with the task (a trivial local edit needs the affected file and
  its direct callers); progress notes go through the host's progress channel when one exists;
  tests, docs, or files needed to complete and verify the requested change are part of it,
  and only unrelated extras become suggestions.
- `CAPABILITIES.md`: set a delegate's model or effort only when the spawn tool exposes that
  argument; routing pointers for Claude, Codex, and Grok; never pass another host's aliases.
- `think-like-fable`: "design it out" applies when a small, in-scope construction removes the
  unverified dependency; otherwise report it.
- Grok adapter: Grok Build discovers `.agents/skills/`, so the `.grok/skills/` wrappers are
  required to keep the skills opt-in; `@` imports are not expanded; the effort table is user
  configuration; `spawn_subagent` takes `model` only when its schema lists it; removed
  unsourced price, context, and routing claims.
- Codex adapter: use only the model IDs and effort values the installed host exposes;
  fallbacks when a pinned model is unavailable.
- Windows: `tools/sdd.py` accepts in-repository paths spelled with 8.3 short names; tests read
  files as UTF-8.
- `README.md`, `tests/BEHAVIORAL_EVALS.md` (Grok loading case) updated; `AGENT_CONTEXT.md`
  regenerated. Details in `VALIDATION.md`.

# Revision: Claude Sonnet 5.5 — 2026-09-29

- Baseline: a real check that exercises changed code before calling it done (syntax-only or
  failed-to-start checks do not count; otherwise say which check did not run and why); ideas,
  options, or a plan are delivered without building; unrequested features, tests, docs, or
  files become suggestions in the final report.
- `MODEL-NOTES.md`: Sonnet 5.5 section (recalibrated effort, `between_tools` thinking, API
  breaking changes, mid-turn message placement, refusal categories); Sonnet 5 marked previous.
- `MODEL-ROUTING.md`: `sonnet` means the host's current Sonnet; Sonnet delegates at `high`
  effort; smaller-model briefs name the check that proves the task done. Tiers unchanged.
- Source [S21]; new contract checks; `AGENT_CONTEXT.md` regenerated.

# Revision: Claude, OpenAI, and Grok model compatibility — 2026-09-28

Adapted the bundle to Anthropic's current prompting guides ([S8]-[S13]) without making the
shared rules model-specific.

- Baseline (`AGENT_RULES.md`): new "Progress updates and ending a turn" section (one line of
  intent, notes with the next tool call, no early stops while authorized work remains,
  assessment-only answers when the user is describing a problem); explore broadly before the
  first edit; targeted edits over rewrites; verification sized to risk, no redundant checks.
- `CAPABILITIES.md`: when to delegate (separable work, isolated context, independent
  review; not for lookups one search answers), explicit model per delegate under a routing
  policy, and fencing of untrusted material passed to delegates. Independent review is
  encouraged for quality-first work and expected for safety-relevant changes; time budgets
  are passed on only when the user sets a deadline (no default time pressure).
- New `adapters/claude-code/MODEL-ROUTING.md` (imported by root `CLAUDE.md`): owner routing
  of delegated work to haiku / sonnet / opus; fable excluded.
- New `adapters/claude-code/MODEL-NOTES.md`: per-model host settings and optional harness
  snippets for Opus 5.5, Opus 5, Sonnet 5, Haiku 4.5, and Fable 5.1.
- Super Code: model placeholders no longer say REQUIRED or point at a nonexistent "Model
  Selection" section; reviewers report every finding with a confidence level (recall for
  Sonnet-class reviewers); "Reasoning:" verdict lines renamed "Rationale:"; continuation
  updates travel with the next dispatch; briefs carry a time budget.
- Inherited references: calmed all-caps MUST/NEVER/STOP/Iron Law wording in the active
  debugging, TDD, verification, and review references (meaning unchanged, reasons added);
  removed a threatening line; added a note on emphatic wording to the skill-writing guides.
- Fable references: discover broad, read narrow; stopping early as a failure mode; time
  budgets; status reports are not stopping points; verbatim constraints in the working log.
- OpenAI/Codex: new `adapters/codex/` with loading notes (32 KiB `AGENTS.md` budget), GPT-6
  Astra/Sol/Luna guidance, and optional `.codex/agents/` files: explorer (luna, read-only),
  implementer (sol, high), reviewer (astra, high, read-only) ([S14]-[S16]).
- Grok: new `adapters/grok-build/` with loading notes (Grok Build reads `AGENTS.md` and
  `CLAUDE.md` but not the project's `.agents/skills/`), opt-in `.grok/skills/` wrappers, and
  effort-based routing for Grok 4.7 ([S17]-[S20]). `MODEL-ROUTING.md` is scoped to Claude.
- Baseline: the user's direct instruction wins over a skill's method/style/scope guidance;
  safety, honesty, and permission limits still hold (GPT-6 Astra weighs skill files heavily).
- Tests: new contract checks for the above; `AGENT_CONTEXT.md` regenerated.

# Revision: portable agent bundle — 2026-09-13

## Shared contract

Added root `AGENTS.md`, Claude Code imports, one agent-neutral baseline, explicit opt-in
activation, and capability-based fallbacks. Added a generated context export for hosts without
filesystem discovery. No model name or special agent tool is required for the prose workflows.
Optional native metadata/adapters do not replace the portable policy or host security controls.

Removed conflicting autoactivation, universal design approvals, automatic pull/commit/cleanup,
and mandatory model/subagent assumptions from the active entry points. Retained Fable's core
reasoning guidance and the reference library. Labeled inherited/vendor examples as subordinate
or historical; restored a clear authority boundary. Ordinary careful work remains the default.

## Helpers

Replaced the three fragile Bash-only task helpers with thin executable wrappers over a
standard-library Python implementation. The plan argument is now required for workspace and
review-package. State moved from worktree-wide `.superpowers/sdd` to identity-scoped
`.agents-state/sdd/...`. Different plans or edits never automatically share completion state.

Added validated task extraction, global-constraint inclusion, fence handling, duplicate-task
rejection, no-clobber output, conservative completion receipts, evidence hashing, status checks,
Git revision validation, and a writer lock. These are recovery checks, not proof of correctness,
cryptographic authentication, a repository lock, or permission to create commits.

Old state is left untouched and not migrated automatically. See `tools/README.md` for the
intentional CLI changes, snapshot limits, source-plan immutability, and manual fallbacks.

## Other corrections

Replaced blanket output de-energization with approved machine-specific safe-state requirements.
Removed the misleading self-checksum audit claim. Corrected the roadmap entry-point name.
Preserved the original `/input` AGV documentation hint as explicitly project-specific context;
left unknown project build commands and architecture facts unfilled rather than guessing.
Added input provenance, documentation sources, deterministic tests, behavioral evaluation cases,
and a validation record. Browser companion, hardware behavior, and live cross-model adherence
remain separate verification tasks, not claimed test results.
