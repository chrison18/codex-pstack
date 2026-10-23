"""Regression coverage for actual v2 research evidence notification shapes."""

import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).with_name('accept-codex-research.py')
spec = importlib.util.spec_from_file_location('research_acceptance', SCRIPT)
research = importlib.util.module_from_spec(spec)
spec.loader.exec_module(research)


class CaptureTest(unittest.TestCase):
    def test_raw_spawn_request_and_resolved_start_are_distinct_and_deduplicated(self):
        events = [{'method': 'rawResponseItem/completed', 'params': {'item': {
            'type': 'function_call', 'name': 'spawn_agent',
            'arguments': '{"task_name":"explainer","agent_type":"poteto-agent","model":"gpt-6.1-sol","reasoning_effort":"low"}'}}}]
        for method in ('item/started', 'item/completed'):
            events.append({'method': method, 'params': {'item': {
                'type': 'subAgentActivity', 'kind': 'started', 'agentThreadId': 'child',
                'model': 'gpt-6-luna', 'reasoningEffort': 'high'}}})
        summary, final = research.summarize_events(events, 'parent')
        self.assertEqual(summary['spawnRequests'], [{'task_name': 'explainer', 'agent_type': 'poteto-agent',
                                                   'model': 'gpt-6.1-sol', 'reasoning_effort': 'low'}])
        self.assertEqual(summary['resolvedAgentStarts'], {'child': {'model': 'gpt-6-luna', 'effort': 'high'}})
        self.assertEqual(final, '')

    def test_final_answer_excludes_child_messages_and_parent_commentary(self):
        def message(thread, phase, text):
            return {'method': 'item/completed', 'params': {'threadId': thread,
                    'item': {'type': 'agentMessage', 'phase': phase, 'text': text}}}
        summary, final = research.summarize_events([
            message('parent', 'commentary', 'Plan'),
            message('child', 'final_answer', 'Unreviewed delegate finding'),
            message('parent', 'final_answer', 'Inspected answer')], 'parent')
        self.assertEqual(final, 'Inspected answer')
        self.assertEqual(summary, {'spawnRequests': [], 'resolvedAgentStarts': {}})


if __name__ == '__main__':
    unittest.main()
