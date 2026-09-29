---
name: execute-plan
description: Execute an implementation plan in this repository (project override of Grok Build's bundled execute-plan). Works in the current working tree under the shared engineering rules; no branches, worktrees, commits, pushes, or PRs unless the user asks for them.
when-to-use: Use when asked to "execute plan", "run the plan", "implement the plan", or "/execute-plan".
---

This project replaces Grok Build's bundled `execute-plan` skill. That skill creates worktrees,
commits, builds a branch stack, and pushes, which this project's rules do not allow without
the user's go-ahead.

Read `.agents/AGENT_RULES.md` from the repository root, then execute the plan the user named:

1. Read the whole plan and the files it touches. Keep a checklist of its tasks.
2. Implement the tasks in order in the current working tree. For each one, run the checks
   the plan or project names (tests, build, type check) and fix failures before moving on.
3. Do not create branches or worktrees, commit, push, or open PRs unless the user explicitly
   asked for that in this task. Leave the changes uncommitted and preserve unrelated work.
4. Finish with the report `AGENT_RULES.md` asks for: what changed per task, the checks you ran
   and their results, and anything left unverified.

If the user explicitly wants Grok's branch-stack workflow, tell them this project overrides
it and that deleting `.grok/skills/execute-plan/` restores the bundled skill.
