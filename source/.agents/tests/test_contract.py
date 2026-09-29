"""Static checks for the portable contract; not live agent-behavior evaluations."""
import ast
import os
from pathlib import Path
import re
import unittest

A = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def test_root_entry_point_and_claude_imports_share_sources(self):
        entry = (A.parent / 'AGENTS.md').read_text(encoding='utf-8')
        adapter = (A.parent / 'CLAUDE.md').read_text(encoding='utf-8')
        for path in ('.agents/AGENT_RULES.md', '.agents/skills/SKILLS.md'):
            self.assertIn(path, entry)
            self.assertIn('@' + path, adapter)
        self.assertIn('@AGENTS.md', adapter)

    def test_shared_skill_frontmatter_is_portable(self):
        for directory in (A / 'skills').iterdir():
            if not directory.is_dir():
                continue
            with self.subTest(skill=directory.name):
                text = (directory / 'SKILL.md').read_text(encoding='utf-8')
                front = text.split('---', 2)[1]
                name = re.search(r'^name: (.+)$', front, re.M)[1]
                self.assertEqual(name, directory.name)
                self.assertRegex(name, r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
                self.assertLessEqual(len(name), 64)
                description = re.search(r'^description: >-\n((?:  .*\n)+)', front, re.M)
                self.assertIsNotNone(description)
                self.assertLessEqual(len(' '.join(line.strip() for line in description[1].splitlines())), 1024)
                self.assertIn('only when the user explicitly', text.lower())
                self.assertNotIn('disable-model-invocation:', front)
                self.assertNotIn('allowed-tools:', front)
                self.assertLess(len(text.splitlines()), 500)

    def test_optional_host_invocation_controls_are_present(self):
        for name in ('think-like-fable', 'super-code'):
            self.assertIn('allow_implicit_invocation: false', (A / 'skills' / name / 'agents/openai.yaml').read_text(encoding='utf-8'))
            self.assertIn('disable-model-invocation: true', (A / 'adapters/claude-code' / name / 'SKILL.md').read_text(encoding='utf-8'))

    def test_no_original_activation_or_pull_conflict(self):
        baseline = (A / 'AGENT_RULES.md').read_text(encoding='utf-8')
        fable = (A / 'skills/think-like-fable/SKILL.md').read_text(encoding='utf-8')
        router = (A / 'skills/super-code/SKILL.md').read_text(encoding='utf-8')
        self.assertNotIn('Always pull and check first', baseline)
        self.assertNotIn("Trigger even when the user doesn't", fable)
        self.assertNotIn("Only skip a skill's workflow when the user has told you to", router)
        self.assertNotIn('Fault states de-energize outputs.', (A / 'skills/think-like-fable/references/twincat-rules.md').read_text(encoding='utf-8'))

    def test_active_router_reference_paths_exist(self):
        for name in ('super-code', 'think-like-fable'):
            directory = A / 'skills' / name
            text = (directory / 'SKILL.md').read_text(encoding='utf-8')
            for relative in re.findall(r'`(references/[^`]+\.md)`', text):
                if '<' not in relative:
                    with self.subTest(path=relative):
                        self.assertTrue((directory / relative).is_file())

    def test_review_package_calls_include_plan_identity(self):
        text = (A / 'skills/super-code/references/subagent-driven-development/subagent-driven-development.md').read_text(encoding='utf-8')
        self.assertNotIn('scripts/review-package BASE HEAD', text)
        self.assertIn('scripts/review-package PLAN_FILE BASE HEAD', text)
        self.assertNotIn('as complete are DONE', text)

    def test_all_reference_docs_have_scope_or_historical_notice(self):
        for path in (A / 'skills/super-code/references').rglob('*.md'):
            with self.subTest(path=str(path)):
                text = path.read_text(encoding='utf-8')
                self.assertTrue('> Scope: use only within' in text or '> Historical/reference material' in text)

    def test_python_helpers_parse_with_python39_grammar(self):
        for path in (A / 'tools').glob('*.py'):
            with self.subTest(path=path.name):
                ast.parse(path.read_text(encoding='utf-8'), filename=str(path), feature_version=(3, 9))

    def test_executable_entry_points_have_lf(self):
        names = {'sdd-workspace', 'task-brief', 'review-package'}
        for path in A.rglob('*'):
            if path.is_file() and (path.suffix == '.sh' or path.name in names or path.parent == A / 'tools' and path.suffix == '.py'):
                with self.subTest(path=str(path)):
                    self.assertNotIn(b'\r\n', path.read_bytes())
                    if os.name == 'posix':
                        self.assertTrue(path.stat().st_mode & 0o111, f'missing executable bit: {path}')


    def test_turn_ending_and_progress_rules_are_in_baseline_and_export(self):
        for path in ('AGENT_RULES.md', 'AGENT_CONTEXT.md'):
            text = (A / path).read_text(encoding='utf-8')
            with self.subTest(path=path):
                self.assertIn('## Progress updates and ending a turn', text)
                self.assertIn('a status note is not a stopping point', text)
                self.assertIn('the deliverable is your assessment', text)

    def test_claude_model_routing_is_imported_and_excludes_fable(self):
        adapter = (A.parent / 'CLAUDE.md').read_text(encoding='utf-8')
        self.assertIn('@.agents/adapters/claude-code/MODEL-ROUTING.md', adapter)
        routing = (A / 'adapters/claude-code/MODEL-ROUTING.md').read_text(encoding='utf-8')
        for alias in ('`haiku`', '`sonnet`', '`opus`'):
            self.assertIn(alias, routing)
        self.assertIn('Do not route work to `fable`', routing)
        self.assertTrue((A / 'adapters/claude-code/MODEL-NOTES.md').is_file())
        entry = (A.parent / 'AGENTS.md').read_text(encoding='utf-8')
        self.assertNotIn('MODEL-ROUTING', entry)  # vendor routing stays out of the shared loader

    def test_no_reasoning_extraction_or_nonexistent_model_section(self):
        refs = A / 'skills/super-code/references'
        for path in list(refs.rglob('*.md')) + list((A / 'skills').glob('*/SKILL.md')):
            text = path.read_text(encoding='utf-8')
            with self.subTest(path=str(path)):
                self.assertNotIn('**Reasoning:**', text)
                self.assertNotIn('per SKILL.md Model Selection', text)

    def test_active_references_avoid_shouted_imperatives(self):
        active = [
            'systematic-debugging/systematic-debugging.md',
            'test-driven-development/test-driven-development.md',
            'verification-before-completion/verification-before-completion.md',
            'receiving-code-review/receiving-code-review.md',
        ]
        for relative in active:
            text = (A / 'skills/super-code/references' / relative).read_text(encoding='utf-8')
            with self.subTest(path=relative):
                self.assertNotRegex(text, r'\b(MANDATORY|Iron Law|You MUST|ALWAYS before|STOP\. Return)\b')

    def test_reviewers_report_uncertain_findings(self):
        for relative in ('subagent-driven-development/task-reviewer-prompt.md',
                         'requesting-code-review/code-reviewer.md'):
            text = (A / 'skills/super-code/references' / relative).read_text(encoding='utf-8')
            with self.subTest(path=relative):
                self.assertIn('including ones you are unsure about', text)

    def test_independent_review_is_encouraged_not_restricted(self):
        for path in ('AGENT_RULES.md', 'CAPABILITIES.md', 'AGENT_CONTEXT.md'):
            text = (A / path).read_text(encoding='utf-8')
            with self.subTest(path=path):
                self.assertIn('independent review', text)
                self.assertNotIn('second opinion on work you can check yourself', text)
        routing = (A / 'adapters/claude-code/MODEL-ROUTING.md').read_text(encoding='utf-8')
        self.assertIn('Independent reviewers are welcome', routing)

    def test_grok_and_codex_adapters(self):
        for name in ('think-like-fable', 'super-code'):
            wrapper = (A / 'adapters/grok-build' / name / 'SKILL.md').read_text(encoding='utf-8')
            with self.subTest(skill=name):
                self.assertIn('disable-model-invocation: true', wrapper)
                self.assertIn(f'name: {name}', wrapper)
                self.assertIn(f'.agents/skills/{name}/SKILL.md', wrapper)
        for path in sorted((A / 'adapters/codex/agents').glob('*.toml')):
            text = path.read_text(encoding='utf-8')
            with self.subTest(agent=path.name):
                for field in ('name = ', 'description = ', 'developer_instructions = ', 'model = '):
                    self.assertIn(field, text)
                self.assertIn('.agents/AGENT_RULES.md', text)
                try:
                    import tomllib
                except ImportError:  # Python < 3.11
                    continue
                self.assertEqual(tomllib.loads(text)['name'], path.stem)
        reviewer = (A / 'adapters/codex/agents/reviewer.toml').read_text(encoding='utf-8')
        self.assertIn('sandbox_mode = "read-only"', reviewer)
        self.assertIn('Claude hosts only', (A / 'adapters/claude-code/MODEL-ROUTING.md').read_text(encoding='utf-8'))

    def test_user_instruction_precedes_skill_guidance(self):
        for path in ('AGENT_RULES.md', 'AGENT_CONTEXT.md'):
            self.assertIn("the user's instruction wins", (A / path).read_text(encoding='utf-8'))

    def test_sonnet_5_5_rules(self):
        for path in ('AGENT_RULES.md', 'AGENT_CONTEXT.md'):
            text = (A / path).read_text(encoding='utf-8')
            with self.subTest(path=path):
                self.assertIn('run a real check that exercises the change', text)
                self.assertIn('ideas, options, or a plan', text)
        notes = (A / 'adapters/claude-code/MODEL-NOTES.md').read_text(encoding='utf-8')
        self.assertIn('claude-sonnet-5-5', notes)
        self.assertIn('Run Sonnet delegates at `high` effort', (A / 'adapters/claude-code/MODEL-ROUTING.md').read_text(encoding='utf-8'))

if __name__ == '__main__':
    unittest.main()
