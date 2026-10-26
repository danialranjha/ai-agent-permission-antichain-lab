import copy
import itertools
import json
from pathlib import Path
import unittest
from experiment import audit

CASES=json.loads(Path(__file__).with_name('fixtures.json').read_text())


def oracle_masks(scope_masks, task_mask):
    # Independent integer-bitmask implementation, no production set operations.
    reachable=set()
    for grant in range(1 << len(scope_masks)):
        union=0
        for i,mask in enumerate(scope_masks):
            if (grant >> i) & 1:
                union |= mask
        if union & task_mask == task_mask:
            reachable.add(union)
    return {x for x in reachable if not any(y != x and (y & x) == y for y in reachable)}


class FootprintTests(unittest.TestCase):
    def test_tradeoff(self):
        r=audit(CASES[0]); self.assertEqual(r['status'],'incomparable_minima')
        self.assertEqual(len(r['intervention_all_minima']),2)
        self.assertEqual(r['control_single_view']['grant'],['project_editor'])
        self.assertEqual(r['explicit_preferences']['operations'],[['project_editor']])
        self.assertEqual(r['explicit_preferences']['writes'],[['organization_reader']])
        self.assertEqual({tuple(x['grant']) for x in r['intervention_all_minima']},{('project_editor',),('organization_reader',)})
        w=r['incomparability_witnesses'][0]
        self.assertTrue(w['left_only']); self.assertTrue(w['right_only'])
        by_name={o['grant'][0]:o['risk'] for o in r['intervention_all_minima']}
        self.assertEqual(by_name['project_editor'],dict(operations=2,writes=1,services=1,admin=0))
        self.assertEqual(by_name['organization_reader'],dict(operations=3,writes=0,services=3,admin=0))

    def test_unique_least_counterfactual(self):
        r=audit(CASES[1]);self.assertEqual(r['status'],'unique_least')
        self.assertEqual(r['intervention_all_minima'][0]['footprint'],['summary.read'])

    def test_aliases_collapse(self):
        r=audit(CASES[2]);self.assertEqual(len(r['intervention_all_minima']),2)
        self.assertIn(['organization_reader'],[x['grant'] for x in r['intervention_all_minima']])
        self.assertNotIn(['reader_alias'],[x['grant'] for x in r['intervention_all_minima']])

    def test_scope_name_minimality_is_insufficient(self):
        r=audit(CASES[3]);self.assertEqual(r['status'],'unique_least')
        self.assertEqual(r['intervention_all_minima'][0]['grant'],['read_directory','read_summary'])
        self.assertNotIn('project.edit',r['intervention_all_minima'][0]['footprint'])

    def test_equal_risk_does_not_collapse_footprints(self):
        r=audit(CASES[4]);opts=r['intervention_all_minima']
        self.assertEqual(len(opts),2);self.assertEqual(opts[0]['risk'],opts[1]['risk'])
        for tied in r['explicit_preferences'].values():self.assertEqual(len(tied),2)
        self.assertEqual(r['risk_dominated_minima'],[])

    def test_risk_dominance_does_not_remove_minimum(self):
        r=audit(CASES[5]);self.assertEqual(len(r['intervention_all_minima']),2)
        self.assertEqual(r['risk_dominated_minima'],[{'grant':['right'],'by':['left']}])

    def test_infeasible(self):
        r=audit(CASES[6]);self.assertEqual(r['status'],'infeasible')
        self.assertIsNone(r['control_single_view']);self.assertEqual(r['intervention_all_minima'],[])

    def test_empty_task(self):
        r=audit(CASES[7]);self.assertEqual(r['status'],'unique_least')
        self.assertEqual(r['intervention_all_minima'][0]['grant'],[])
        self.assertEqual(r['intervention_all_minima'][0]['footprint'],[])

    def test_order_invariance(self):
        for c in CASES:
            reversed_case=copy.deepcopy(c)
            reversed_case['scopes']=dict(reversed(list(c['scopes'].items())))
            self.assertEqual(audit(c),audit(reversed_case))

    def test_invalid_input_fails(self):
        for mutate in [lambda c:c['scopes'].update(bad=['UNKNOWN']),
                       lambda c:c.update(task=['UNKNOWN']),
                       lambda c:c['operations']['summary.read'].update(write='false'),
                       lambda c:c['scopes'].update({f's{i}':[] for i in range(13)})]:
            c=copy.deepcopy(CASES[0]); mutate(c)
            with self.assertRaises(ValueError):audit(c)

    def test_exhaustive_independent_oracle(self):
        names=['a','b','c'];ops={n:dict(service='toy',write=False,admin=False) for n in names}
        checked=0
        for masks in itertools.product(range(8),repeat=3):
            scopes={f's{i}':[n for bit,n in enumerate(names) if mask&(1<<bit)] for i,mask in enumerate(masks)}
            for task in range(8):
                c=dict(id='exhaustive',operations=ops,scopes=scopes,task=[n for bit,n in enumerate(names) if task&(1<<bit)])
                got={sum(1<<names.index(n) for n in o['footprint']) for o in audit(c)['intervention_all_minima']}
                self.assertEqual(got,oracle_masks(masks,task),(masks,task));checked+=1
        self.assertEqual(checked,4096)

if __name__=='__main__':unittest.main()
