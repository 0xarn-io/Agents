# Optional Claude Code skill wrappers

File-based loading through root `CLAUDE.md` works without these wrappers. To expose native
slash commands, copy each `<name>/SKILL.md` from here to
`.claude/skills/<name>/SKILL.md` in the project. Merge rather than overwrite an existing skill.
These wrappers use a Claude Code-specific invocation flag; shared skills stay format-neutral.
Keep `.agents/` at the repository root. Wrappers read the canonical source instead of copying it.

Source: `.agents/SOURCES.md` [S6]. Test loading and invocation in the installed Claude Code host.

`MODEL-ROUTING.md` is the owner's model-routing preference for delegated work (haiku for
mechanical tasks, sonnet for small well-specified ones, opus for medium-to-hard work, no
fable). Root `CLAUDE.md` imports it, so it applies in every Claude Code session in this
repository; it has no effect on hosts that cannot choose a model per delegate.
`MODEL-NOTES.md` is reference material for configuring hosts, harnesses, and API apps for
current Claude models (Opus 5.5, Opus 5, Sonnet 5.5, Sonnet 5, Haiku 4.5, Fable 5.1). It is not loaded
automatically. Sources: `.agents/SOURCES.md` [S8]-[S13].
