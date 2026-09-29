# Shared repository instructions

@AGENTS.md
@.agents/AGENT_RULES.md
@.agents/skills/SKILLS.md
@.agents/adapters/claude-code/MODEL-ROUTING.md

These imports use the same sources as other agents; do not maintain a separate rulebook here.
Where the host expands these imports (Claude Code), `AGENT_RULES.md` and `skills/SKILLS.md`
are already loaded; do not read them again. A host that shows the `@` lines as plain text
should read the listed files.
The model-routing file is a Claude-specific owner preference for delegated work only.
Load optional skill bodies only after activation under the shared skill policy.
