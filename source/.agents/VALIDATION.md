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
`tests/BEHAVIORAL_EVALS.md` still need running in each host.

---

# Validation record — 2026-09-29 (Claude Sonnet 5.5 update)

62 deterministic unit/contract tests passed (61 from the 2026-09-28 revision + 1 for the
Sonnet 5.5 rules). `AGENT_CONTEXT.md` regenerated and matches canonical sources. No live
Sonnet 5.5 session was run; behavior is from [S21].

---

# Validation record — 2026-09-28 (Claude, OpenAI, and Grok compatibility revision)

61 deterministic unit/contract tests passed in one run (53 existing + 8 new contract tests
for the turn-ending rules, Claude model routing, independent review being kept, reviewer
recall wording, calmed imperatives, absence of reasoning-extraction wording, the Grok Build
wrappers and Codex agent files, and user-over-skill precedence). A mutation check
(reinstating "MANDATORY" in the TDD reference and allowing fable in the routing file) made
the two relevant tests fail as intended. The three Codex agent files parse as TOML with the
required fields. `AGENT_CONTEXT.md` was regenerated and matches the canonical sources.

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
