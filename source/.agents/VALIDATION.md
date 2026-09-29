# Current status (read this first)

As of 2026-09-29 (release v2026.09.29.4):

- **Live behavioral evals: run.** 12 cases in real headless sessions of Claude Code 2.1.284
  (Opus 5.5, Sonnet 5.5), Codex CLI 0.153.4 (GPT-6 Astra), and Grok Build 1.0.44 (Grok 4.7),
  on Windows 11, with and without the bundle. In the final round, 56 of 56 runs with the bundle
  passed. Harness and full results: `evals/` in the repository.
- **Live reviews: run.** Grok 4.7 and GPT-6 Astra reviewed the bundle in their own hosts over
  several rounds; final ratings Grok 9.0/10 and GPT-6 Astra 9.3/10, both "good for all".
- **Deterministic tests:** 64 bundle tests and 16 eval-grader tests, run in CI on Linux,
  Windows, and macOS with Python 3.9 and 3.13.
- **Not established:** other models and hosts, other operating systems for the live evals,
  larger or real projects (the fixture is small, 2 runs per case), the browser companion and
  Graphviz output, and physical machinery.

Records below are in reverse date order. Older records describe what was true when they were
written; statements they make that later work overturned are marked "Superseded".

---

# Validation record — 2026-09-29 (ratings after the eval fixes)

(Asked again from scratch after v2026.09.29.4, without anchoring on these scores: Grok 4.7
9.0/10, GPT-6 Astra 9.3/10, both "AGREE: GOOD FOR ALL". See "Current status".)

Re-rated read-only after the eval-driven fixes: Grok 4.7 went from 8.0 to 8.7 to 9.2 to 9.6/10,
and GPT-6 Astra from 8.2 to 8.7 to 9.0 to 9.7/10. Both ended with "AGREE: GOOD FOR ALL", and
Claude Opus 5.5 agrees. The last rounds fixed uncommitted-work review (`review-package
BASE WORKTREE`) and the eval grader, which now counts a check only when a shell started it and
its output proves it ran (14 grader tests in the repository's `evals/`). After a final re-grade,
every code-changing eval run either ran a real check or said it could not. 64 bundle tests pass.

---

# Validation record — 2026-09-29 (fixes from the Grok and GPT ratings)

63 deterministic tests passed (1 skipped on Windows). Behavioral matrix with the repository's
`evals/run_evals.py`: 9 cases x 4 models (Opus 5.5, Sonnet 5.5, GPT-6 Astra, Grok 4.7) x 2
runs, plus 6 cases without the bundle as a control (120 runs), graded separately on artifact,
verification, and handoff; then re-runs of C6, C8, and C9 after the fixes below. With the
final bundle, six cases passed in all 8 runs; Opus reported the injected instruction in 3 of
4 runs, Grok stopped at a requested plan in 3 of 4 (the miss came from its host plan mode being
auto-approved in a headless run), and Grok executed a plan cleanly in 2 of 2 after the
override. The runs found three problems, addressed here: Grok Build's bundled `execute-plan`
committed, branched, and tried to push; Grok treated a plan request as work to finish; and
Opus sometimes did not report an injected instruction. The last two still occur occasionally. Full tables and host findings: `evals/README.md` in the repository.

---

# Validation record — 2026-09-29 (behavioral evals in three hosts)

First behavioral run: 7 cases from `tests/BEHAVIORAL_EVALS.md`, automated by the repository's
`evals/run_evals.py`, on Claude Opus 5.5 and Sonnet 5.5 (Claude Code 2.1.284), GPT-6 Astra
(Codex CLI 0.153.4), and Grok 4.7 (Grok Build 1.0.44), on Windows 11. That is 28 runs in
disposable fixture repositories, judged on actual git state and transcripts. 26 passed. In
the other 2, Opus and Grok did not act on an injected log instruction but did not report it
either. After the new reporting rule in `AGENT_RULES.md`, 8 of 8 re-runs passed. Full table
and harness caveats: `evals/README.md` in the repository. Deterministic tests: 62 passed.

---

# Validation record — 2026-09-29 (three-model review: Claude, Grok, GPT)

62 deterministic unit/contract tests passed on Windows 11 with Python 3.14 and Git, using the
default temp directory (an 8.3 short path) and no `PYTHONUTF8` override. Before this revision,
42 of them failed on Windows: the tests read files with the locale encoding, and
`tools/sdd.py` rejected in-repository paths spelled with 8.3 short names. Both are fixed.
One test is skipped on Windows (POSIX executable bits). `AGENT_CONTEXT.md` regenerated.

Read-only review, same prompt, each model in its own host:

| Model / host | Round 1 | Round 2 | Round 3 | Round 4 |
|---|---|---|---|---|
| Claude Opus 5.5 / Claude Code | Changes proposed and applied | Applied fixes | Applied fixes | Agree |
| Grok 4.7, effort `high` / Grok Build 1.0.44 (`grok -p`, plan mode) | Needs changes | Disagree (2 items) | Disagree (2 items) | **Agree: good for all** |
| GPT-6 Astra, effort `high` / Codex CLI 0.153.4 (`codex exec -s read-only`) | Needs changes | Disagree (1 item) | **Agree: good for all** | **Agree: good for all** |

Grok corrected one of its own round-1 host claims in round 3 after checking its installed
guide; the disputed claims were removed rather than restated. Headless Grok runs in plan mode
end with `stop_reason: cancelled` when the model calls the shell tool; give it exact paths so
it can use `read_file` only. These are reviews, not behavioral tests: the cases in
`tests/BEHAVIORAL_EVALS.md` still need running in each host. (They were run later the same
day; see the records above.)

---

# Validation record — 2026-09-29 (Claude Sonnet 5.5 update)

62 deterministic unit/contract tests passed (61 from the 2026-09-28 revision + 1 for the
Sonnet 5.5 rules). `AGENT_CONTEXT.md` regenerated and matches canonical sources. No live
Sonnet 5.5 session was run; behavior is from [S21]. (Superseded later the same day: Sonnet 5.5
ran in every behavioral eval round.)

---

# Validation record — 2026-09-28 (Claude, OpenAI, and Grok compatibility revision)

61 deterministic unit/contract tests passed in one run (53 existing + 8 new contract tests
for the turn-ending rules, Claude model routing, independent review being kept, reviewer
recall wording, calmed imperatives, absence of reasoning-extraction wording, the Grok Build
wrappers and Codex agent files, and user-over-skill precedence). A mutation check
(reinstating "MANDATORY" in the TDD reference and allowing fable in the routing file) made
the two relevant tests fail as intended. The three Codex agent files parse as TOML with the
required fields. `AGENT_CONTEXT.md` was regenerated and matches the canonical sources.

> Superseded on 2026-09-29 by live sessions in all three hosts; see "Current status" at the top.

Not executed: no live Claude Code, Codex, Grok Build, or API sessions with any model.
Model and host behavior is taken from vendor documentation in `SOURCES.md` [S8]-[S20].
Grok Build's per-subagent fields are undocumented publicly, so no Grok agent files are
shipped. Confirm with the new cases in `tests/BEHAVIORAL_EVALS.md`.
Environment: Linux x86_64, Python 3.11, Git available.

---

# Validation record — 2026-09-13

## Executed checks

53 distinct deterministic unit/contract tests passed, with no failures or skips, in four
isolated test groups (14 + 13 + 13 + 13). The nine static contract tests were re-run after
the final lower-level wording corrections and passed again. Two earlier monolithic runner
attempts hit execution time limits; they were not counted as completed suites. The full
53-test set was subsequently completed in the four groups recorded below.

The tests exercise default helper paths, executable-bit loss, spaces in paths, plan isolation,
changed plans, global constraints, fenced headings, malformed/duplicate tasks, multi-commit
review packages, dirty worktrees, stale HEAD, changed/missing/corrupt evidence, receipt identity,
invalid revisions, non-clobbering output, symlink/traversal rejection, locks, and context export.
They create Git commits only inside temporary fixtures, never in the user's repository.

Additional checks passed:

- Six Bash syntax checks and three JavaScript/CommonJS syntax checks (nine total).
- All four new Python files parsed using Python 3.9 grammar.
- Actual YAML parsing and field validation for the two shared skills and two optional Claude
  wrappers; both optional OpenAI metadata files parsed with implicit invocation disabled.
- Concrete local Markdown links in active documents resolved. Historical illustrative links
  were excluded, not asserted to be valid current resources.
- The generated AGENT_CONTEXT.md exactly matched the canonical baseline sources.

Execution environment: Linux x86_64; Python 3.13.5; Git 2.47.3; Bash 5.2.37;
Node.js 22.16.0. Python 3.9 grammar validation is not a runtime test on Python 3.9.
Optional format checks used the environment's YAML parser; the shipped helpers and unit tests
require only Python's standard library, Git, and Bash for the wrapper-specific test.

## Not executed or established

> Superseded on 2026-09-29: live sessions were then run in Claude Code, Codex, and Grok Build,
> and the tests run on Windows, macOS, and Linux in CI. See "Current status" at the top.

No live Claude Code, Grok, GPT/Codex, or other provider-model sessions were run. Host loading
was checked against the official documentation in SOURCES.md, not proven by a live client.
The manual cases in tests/BEHAVIORAL_EVALS.md remain behavioral tests to run in deployment.

Native Windows and macOS execution, browser/visual-companion runtime, Graphviz output,
project application tests, and physical machinery behavior were not exercised. Optional
Node/Bash reference utilities were syntax-checked, not comprehensively audited for security.
No target-project build commands or machine-specific safe-state requirements were supplied.

Markdown guidance does not enforce tool permissions, guarantee identical model behavior,
or prove correct code. Completion receipts validate identity/evidence consistency at a
snapshot; they do not authenticate reviews/tests or lock the repository against later changes.

## Reproduce

From the installed repository root:

```sh
python -m unittest discover -s .agents/tests -p 'test_*.py' -v
```

Use the appropriate Python 3.9+ invocation for the operating system. Bash wrapper tests skip
when Bash is unavailable; symlink tests may skip on platforms lacking symlink permission.
See tests/TEST_RESULTS.txt for the actual completed runs used for this distribution.
