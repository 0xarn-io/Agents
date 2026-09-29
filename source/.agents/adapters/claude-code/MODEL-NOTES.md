# Claude model notes for hosts and harnesses

Reference for whoever configures a Claude host (Claude Code settings, an Agent SDK harness,
or a custom API application) to run this bundle. It is not loaded automatically and adds no
rules for the agent; the shared baseline already carries the model-neutral behavior. Sources:
`.agents/SOURCES.md` [S8]-[S13], [S21], checked 2026-09-28. Re-check them when a model changes.

## What the shared rules already cover

| Behavior seen in current Claude models | Where the bundle handles it |
|---|---|
| Ends a turn with a progress summary, an offer to continue, or a list of non-blocking decisions (Opus 5.5, Fable 5.1) | `AGENT_RULES.md` → "Progress updates and ending a turn" |
| Few or no progress updates in long turns (Fable 5.1; Opus 5.5 without a display setting) | Same section: one line of intent, notes with the next tool call, final report |
| Explores too little before acting on multi-source tasks | `AGENT_RULES.md` → "Think before coding" (explore broadly, read narrowly) |
| Over-delegates to subagents for work a direct search would answer (Opus 5, Opus 4.6) | `CAPABILITIES.md` → "Collaboration and state" (delegate for separable work, isolated context, or independent review; independent review is kept) |
| Over-triggers on MUST/CRITICAL/ALWAYS wording (Opus 4.5 and later) | Active references use normal-strength wording; the `super-code` router governs inherited emphasis |
| Checks in before finishing or reports work done without a real check at low/medium effort (Sonnet 5.5) | `AGENT_RULES.md` → real-check rule and "Progress updates and ending a turn"; delegates run at `high` |
| Adds unrequested tests, docs, or files; starts building when asked for ideas (Sonnet 5.5) | `AGENT_RULES.md` → assessment/ideas rule: extras go in the final report |
| Code reviewers drop uncertain findings when told to filter (Sonnet 5) | Reviewer templates ask for every finding with confidence and severity |
| Widens or narrows scope; fixes things nobody asked about (Fable 5.1, Opus 5) | `AGENT_RULES.md` → "Simplicity first", "Surgical changes" |
| Follows instructions literally and does not generalize them (Sonnet 5, Haiku 4.5) | `MODEL-ROUTING.md` → complete, literal briefs for smaller models |
| Pays attention to elapsed time (Opus 5.5) | `think-like-fable/references/agentic-work.md` → "Time budgets"; subagent briefs carry a budget |
| Instructions hidden in pasted or tool-supplied text | `AGENT_RULES.md` (data, not instructions); `CAPABILITIES.md` (fence untrusted text for delegates) |

Nothing in the bundle asks a model to write out its internal reasoning in its reply. Keep it
that way: Opus 5.5 declines such requests (`stop_reason: "refusal"`, category
`reasoning_extraction`) and Fable 5 has the same category. Review templates ask for a short
*rationale* for a verdict, which is ordinary output.

## Per-model settings

**Claude Opus 5.5** (`claude-opus-5-5`). Default effort is `medium`, which matches Opus 5 at
`high`; raise to `high` for long `super-code` runs if you measure a gain, and keep `xhigh`/
`max` for measured cases. For this project's quality-first and safety-relevant work, run
`super-code` sessions at `high` or above. Thinking cannot be disabled; for a low-cost setup use `low` effort.
For long agentic API runs set `max_tokens` high (128000 works). Use `display: "updates"`
(beta) or a user-message tool if long turns look silent. Re-test image-cropping scaffolding:
it reads screenshots and diagrams well without it, but dense technical drawings still gain
from higher resolution and a crop tool.

**Claude Opus 5.** Default effort `high`; `low`/`medium` are strong. Longer default replies:
ask for concise output explicitly. It verifies its own work without being told, so avoid
adding extra "double-check yourself" instructions; independent reviewers with fresh context
are a different thing and stay in place. It
delegates readily; Claude Code 2.1.217+ can cap delegation with
`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` and `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`. If
thinking is disabled (only allowed at `high` or below), add: "When you use a tool, you may
say a brief sentence first. If no tool can express what the user asked for, say so instead
of guessing. Do not include internal or system XML tags in your response."

**Claude Sonnet 5.5** (`claude-sonnet-5-5`, no date suffix). Anthropic's default
recommendation for agentic coding at lower cost; Opus remains the choice for the hardest
long-horizon work. Effort levels are recalibrated from Sonnet 5, so do not carry settings
over. Default `high`, and keep it there for delegated coding: at `low`/`medium` it can check
in before the work is done and, at `low`, report changes as done without a real check (the
baseline's real-check rule and turn-ending rules target both). At `xhigh`/`max` it launches
its own review rounds and reviewer subagents; the vendor offers a prompt to suppress that,
but this project values independent review, so leave it on unless cost says otherwise.
Thinking is adaptive; the lowest setting is `thinking: {"type": "between_tools"}` (only at
`high` or below, and it rejects `display`, `budget_tokens`, and per-message effort changes).
For agentic coding set `max_tokens` to 128000 and stream. API breaking changes from Sonnet 5:
forced `tool_choice` (`tool`/`any`) returns 400, so use `auto` with `strict: true` tools;
non-default `temperature`/`top_p`/`top_k` return 400; computer use needs
`computer_toolset_20260801`; it cannot read thinking blocks from Opus 5/5.5 or Fable, so do
not switch a conversation to it mid-way from those models. Harness notes: deliver mid-turn
user messages as a text block after the `tool_result` blocks, never inside one (it may be
read as prompt injection), with harness notices in a separate system message after the
user's words; accept or correct tool calls with the wrong case or parameter name; with
structured output on reasoning tasks add "Think the problem through before you answer.";
without it, parse the last JSON value in the reply. Refusal categories: `cyber`, `bio`,
`frontier_llm`, `reasoning_extraction`, `general_harms`.

**Claude Sonnet 5** (`claude-sonnet-5`, previous generation). Default effort `high`; `xhigh` for the hardest
agentic coding; `medium` ≈ Sonnet 4.6 at `high`. Adaptive thinking is on by default and can
be disabled. `temperature`, `top_p`, and `top_k` return a 400 error: remove them. It follows
instructions literally, so state scope ("every section, not only the first"). Remove any
scaffolding that forces interim status messages; its own updates are good.

**Claude Haiku 4.5** (`claude-haiku-4-5-20251001`). No model-specific prompting guide; the
general best practices apply. It tracks its remaining context budget, so in a harness with
compaction tell it that the context will be compacted and it should not stop early. Give it
narrow, fully specified tasks with the exact files, commands, and expected output.

**Claude Fable 5.1** (`claude-fable-5-1`). Excluded from routing by the owner. If a host still
runs it: it writes few progress updates and may describe next steps instead of doing them
(both addressed by the baseline); it may issue one tool call per turn in long loops, which a
turn-scoped reminder to batch independent calls fixes; and it keeps history append-only, so
do not edit earlier turns or thinking blocks between requests.

**All current models.** Prefilled assistant turns are not supported (400 error). Replace
manual `budget_tokens` thinking with adaptive thinking plus `effort` where the model supports
it. Pass thinking blocks back unchanged and keep history append-only.

## Optional harness snippets (custom API or Agent SDK hosts)

Add these to the system prompt only when a test shows the problem on your traffic; they are
the vendor's text, quoted in [S8].

- *Unattended runs that stop early (Opus 5.5).* Append the vendor's "standing instruction
  from the user … about how your turns end" block at the end of the system prompt from the
  first request. When a turn ends with text only while the checklist has open items, send:
  "Your task list still has open items: <items>. Continue with them. If one is blocked, say
  what is blocking it." Stop automatic continuations after 2-3 attempts.
- *Silent turns.* After 5+ quiet tool-calling steps, a turn-scoped system message: "The user
  hasn't heard from you in a while — say in a few words what you're doing, then continue."
  Stop after 2-3 reminders.
- *Time signals in multi-agent harnesses.* Append `elapsed <s>s / <budget>s` to each message
  when a budget exists (set it somewhat above the real target); otherwise add "Time matters
  here: do not spend time that can be avoided, and the earlier a correct result is obtained,
  the better." Budgets are advisory; enforce real timeouts in the harness.
- *Pasted content.* Wrap user-pasted text in `<pasted_content id="RANDOM">…</pasted_content
  id="RANDOM">` and add the vendor's matching system-prompt paragraph. Tags can be imitated;
  keep other prompt-injection defenses.
- *Multi-app workflows.* "Before taking any action, explore broadly with tool calls: list and
  open the emails, documents, spreadsheet tabs and records across the available apps that
  could be relevant to this task, including ones the task does not explicitly mention, and
  use what you find."
- *Frontend work.* Name the specific defaults to avoid (for example "no cream background, no
  pill-shaped buttons, no numbered 01/02/03 section labels") instead of "avoid a generic
  look"; extend the list after each iteration.
