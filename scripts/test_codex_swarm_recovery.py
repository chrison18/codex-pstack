"""Regression checks for actual fault injection and race/conflict evidence instruments."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('accept-codex-swarm-recovery.py').resolve()
spec = importlib.util.spec_from_file_location('recovery_acceptance', SCRIPT)
fixture = importlib.util.module_from_spec(spec); spec.loader.exec_module(fixture)


class RecoveryInstrumentTest(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(); self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name).resolve()
        self.base = 'a' * 40
        self.report = {'baseSha': self.base, 'total': 11,
            'checks': [{'kind':'empty','result':0,'note':'extra annotation permitted'}, {'kind':'zero','result':0},
                       {'kind':'negative','result':'ValueError'}, {'kind':'ordinary','result':11}],
            'method': {'sampleCount':1,'sampleDefinition':'one four-case batch','order':'empty,zero,negative,ordinary'},
            'commands':['python3 -B -c \"from calc import quote; print(quote([]))\"'],
            'extraChecks': [{'items':[{'price':2,'quantity':3}],'result':6}, {'items':[{'price':7,'quantity':-1}],'result':'ValueError'}]}

    def invoke(self, operation, arm=None, stage=None):
        return fixture.operation(self.root, argparse.Namespace(operation=operation,arm=arm,stage=stage))

    def test_quality_ranking_does_not_make_a_wrong_total_eligible(self):
        self.assertEqual(fixture.grade(self.report,self.base), {'valid':True,'score':6})
        self.assertFalse(fixture.grade([],self.base)['valid'])
        missing = copy.deepcopy(self.report); missing.pop('commands')
        self.assertFalse(fixture.grade(missing,self.base)['valid'])
        missing['commands'] = ['python3 -B -c COMMAND']
        self.assertFalse(fixture.grade(missing,self.base)['valid'])
        lean = copy.deepcopy(self.report); lean.pop('extraChecks')
        self.assertEqual(fixture.grade(lean,self.base), {'valid':True,'score':4})
        wrong = copy.deepcopy(self.report); wrong['total'] = 12
        self.assertFalse(fixture.grade(wrong,self.base)['valid'])
        wrong = copy.deepcopy(self.report); wrong.pop('method')
        self.assertFalse(fixture.grade(wrong,self.base)['valid'])

    def test_interrupt_must_target_running_dropout(self):
        def events(target, previous):
            items = [{'type':'function_call','name':'interrupt_agent','call_id':'id','arguments':json.dumps({'target':target})},
                     {'type':'function_call_output','call_id':'id','output':json.dumps({'previous_status':previous})}]
            return [{'method':'rawResponseItem/completed','params':{'item':i}} for i in items]
        self.assertTrue(fixture.interrupted_running_dropout(events('dropout','running')))
        self.assertFalse(fixture.interrupted_running_dropout(events('healthy','running')))
        self.assertFalse(fixture.interrupted_running_dropout(events('dropout',{'completed':'done'})))

    def test_real_report_truncation_and_one_retry_budget(self):
        fixture.save(self.root/'contract.json', {'case':'recovery','baseSha':self.base})
        for arm in ('once','twice'):
            folder = self.root/'cases'/arm
            fixture.save(folder/'proposal.json',self.report)
            self.invoke('publish',arm)
            self.assertFalse(fixture.grade(json.loads((folder/'report-1.json').read_text()),self.base)['valid'])
            self.invoke('publish',arm)
            self.assertEqual(fixture.grade(json.loads((folder/'report-2.json').read_text()),self.base)['valid'],arm=='once')
            with self.assertRaisesRegex(AssertionError,'Retry budget'):
                self.invoke('publish',arm)
            self.assertEqual(len(list(folder.glob('receipt-*.json'))),2)

    def test_rule_cannot_be_declared_after_real_submission(self):
        fixture.save(self.root/'contract.json', {'case':'race','baseSha':self.base})
        self.invoke('declare',stage='first-pass')
        folder = self.root/'cases/first-pass/a'; fixture.save(folder/'proposal.json',self.report)
        self.invoke('publish','a','first-pass')
        self.assertFalse(fixture.grade(json.loads((folder/'report-1.json').read_text()),self.base)['valid'])
        with self.assertRaisesRegex(AssertionError,'Declare before'):
            self.invoke('declare',stage='first-pass')

    def test_tied_races_follow_declared_order_not_completion_order(self):
        entry = SCRIPT.parent.parent/'plugins/pstack/skills/poteto-mode'
        contract = fixture.prepare(self.root,'race-ties',entry)
        workspace=Path(contract['workspace'])
        before={'workspace':fixture.snapshot(workspace)}
        heads={'workspace':fixture.git(workspace,'rev-parse','HEAD')}
        indexes={'workspace':fixture.git(workspace,'diff','--cached','--binary')}
        report=copy.deepcopy(self.report);report['baseSha']=contract['baseSha']
        for stage in ('rank-all','best-of'):
            self.invoke('declare',stage=stage)
            for arm in ('b','a'):
                folder=self.root/'cases'/stage/arm
                fixture.save(folder/'proposal.json',report)
                self.invoke('publish',arm,stage)
                self.assertEqual(fixture.grade(json.loads((folder/'report-1.json').read_text()),contract['baseSha']),{'valid':True,'score':4})
            fixture.save(self.root/'cases'/stage/'selection.json',{'rule':stage,'selected':['a','b'] if stage=='rank-all' else ['a'],'drained':['a','b'],'invalid':[]})
        result=fixture.audit(self.root,contract,[],None,'completed',before,heads,indexes)
        self.assertTrue(result['artifactChecksPassed'])
        for stage,wrong in [('rank-all',['b','a']),('best-of',['b'])]:
            with self.subTest(stage=stage):
                path=self.root/'cases'/stage/'selection.json'
                selected=json.loads(path.read_text());selected['selected']=wrong;fixture.save(path,selected)
                result=fixture.audit(self.root,contract,[],None,'completed',before,heads,indexes)
                self.assertFalse(result['checks'][stage])
                self.assertFalse(result['artifactChecksPassed'])
                selected['selected']=['a','b'] if stage=='rank-all' else ['a'];fixture.save(path,selected)

    def test_second_git_patch_actually_conflicts_without_partial_apply(self):
        entry = SCRIPT.parent.parent/'plugins/pstack/skills/poteto-mode'
        contract = fixture.prepare(self.root,'conflict',entry)
        a = Path(contract['workers']['a']); b = Path(contract['workers']['b'])
        (a/'calc.py').write_text('def total(values):\n    values=list(values)\n    if any(x<0 for x in values): raise ValueError\n    return sum(values)\n')
        (b/'calc.py').write_text('def total(values, fee=0):\n    return sum(values)+fee\n')
        self.assertEqual(self.invoke('apply-a'),0)
        target = Path(contract['integration'])/'calc.py'; before = target.read_bytes()
        self.assertNotEqual(self.invoke('check-b'),0)
        self.assertEqual(target.read_bytes(),before)
        receipt = json.loads((self.root/'reports/check-b.json').read_text())
        self.assertIn('patch',receipt['stderr'])


if __name__=='__main__': unittest.main()
