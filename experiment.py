"""Exhaustive finite authority-footprint audit; never executes an operation."""
import itertools
import json
from pathlib import Path


def validate(case):
    ops, scopes, task = case['operations'], case['scopes'], case['task']
    if not isinstance(ops, dict) or not isinstance(scopes, dict) or not isinstance(task, list):
        raise ValueError('operations/scopes must be objects and task a list')
    if len(scopes) > 12:
        raise ValueError('more than 12 scopes: exhaustive audit refused')
    for name, meta in ops.items():
        if not isinstance(name, str) or not name or not isinstance(meta, dict):
            raise ValueError('invalid operation')
        if (not isinstance(meta.get('service'), str) or not meta['service']
                or type(meta.get('write')) is not bool or type(meta.get('admin')) is not bool):
            raise ValueError('invalid operation metadata')
    for name, members in scopes.items():
        if not isinstance(name, str) or not name or not isinstance(members, list):
            raise ValueError('invalid scope')
        if any(not isinstance(x, str) or x not in ops for x in members):
            raise ValueError('unknown scope operation')
    if any(not isinstance(x, str) or x not in ops for x in task):
        raise ValueError('unknown task operation')


def enumerate_minima(case):
    validate(case)
    names = sorted(case['scopes'])
    task = set(case['task'])
    representatives = {}
    sufficient_grants = 0
    for size in range(len(names) + 1):
        for grant in itertools.combinations(names, size):
            footprint = frozenset().union(*(case['scopes'][name] for name in grant))
            if not task <= footprint:
                continue
            sufficient_grants += 1
            # Size-first, lexicographic iteration makes this representative canonical.
            representatives.setdefault(footprint, grant)
    minima = [f for f in representatives if not any(g < f for g in representatives)]
    minima.sort(key=lambda f: tuple(sorted(f)))
    return names, sufficient_grants, representatives, minima


def risk(footprint, operations):
    return {'operations': len(footprint),
            'writes': sum(operations[x]['write'] for x in footprint),
            'services': len({operations[x]['service'] for x in footprint}),
            'admin': int(any(operations[x]['admin'] for x in footprint))}


def audit(case):
    names, sufficient_grants, representatives, minima = enumerate_minima(case)
    options = [{'grant': list(representatives[f]), 'footprint': sorted(f),
                'extras': sorted(f - set(case['task'])),
                'risk': risk(f, case['operations'])} for f in minima]
    # Deliberately limited control view: one cardinality-preferred minimal grant.
    control = min(options, key=lambda o: (o['risk']['operations'], o['grant'])) if options else None
    preferences = {}
    for metric in ['operations', 'writes', 'services', 'admin']:
        best = min((o['risk'][metric] for o in options), default=None)
        preferences[metric] = [o['grant'] for o in options if o['risk'][metric] == best]
    witnesses = []
    for left, right in itertools.combinations(options, 2):
        lf, rf = set(left['footprint']), set(right['footprint'])
        witnesses.append({'left': left['grant'], 'right': right['grant'],
                          'left_only': sorted(lf-rf), 'right_only': sorted(rf-lf)})
    dominated_risk = []
    for candidate in options:
        for alternative in options:
            a, b = alternative['risk'], candidate['risk']
            if all(a[k] <= b[k] for k in a) and any(a[k] < b[k] for k in a):
                dominated_risk.append({'grant': candidate['grant'], 'by': alternative['grant']})
    return {'id': case['id'], 'task': sorted(set(case['task'])),
            'scope_subsets_enumerated': 2**len(names),
            'sufficient_grants': sufficient_grants,
            'distinct_sufficient_footprints': len(representatives),
            'status': 'infeasible' if not options else 'unique_least' if len(options)==1 else 'incomparable_minima',
            'control_single_view': control, 'intervention_all_minima': options,
            'explicit_preferences': preferences, 'incomparability_witnesses': witnesses,
            'risk_dominated_minima': dominated_risk}


def evidence(rows):
    lines = ['# Exact finite-catalogue evidence', '',
             'Synthetic operation names only. No model, API, token or action ran. Counts enumerate designed catalogues, not sampled attacks.', '',
             '| Scenario | Scope subsets | Sufficient grants | Distinct sufficient footprints | Minimal footprints | Status |',
             '|---|---:|---:|---:|---:|---|']
    for r in rows:
        lines.append(f"| {r['id']} | {r['scope_subsets_enumerated']} | {r['sufficient_grants']} | {r['distinct_sufficient_footprints']} | {len(r['intervention_all_minima'])} | {r['status']} |")
    for r in rows:
        lines += ['', '## '+r['id'], '', 'Task: '+repr(r['task']), '',
                  'Control shows: '+repr(r['control_single_view']), '',
                  '| Grant | Footprint | Extra operations | Operations / writes / services / admin |',
                  '|---|---|---|---|']
        for o in r['intervention_all_minima']:
            v=o['risk']
            lines.append(f"| {', '.join(o['grant']) or '(empty)'} | {', '.join(o['footprint']) or '(empty)'} | {', '.join(o['extras']) or '(none)'} | {v['operations']} / {v['writes']} / {v['services']} / {v['admin']} |")
        lines += ['', 'Declared-preference ties are preserved: '+json.dumps(r['explicit_preferences'],sort_keys=True),
                  '', 'Exclusive-operation witnesses: '+json.dumps(r['incomparability_witnesses'],sort_keys=True),
                  '', 'Risk-vector dominated minima (not footprint containment): '+json.dumps(r['risk_dominated_minima'],sort_keys=True)]
    return '\n'.join(lines)+'\n'


def main():
    root=Path(__file__).resolve().parent
    cases=json.loads((root/'fixtures.json').read_text())
    rows=[audit(c) for c in cases]
    payload={'schema_version':1,'kind':'synthetic_exact_enumeration','model_calls':0,
             'executed_operations':0,'case_count':len(rows),'cases':rows}
    target=root/'artifacts'; target.mkdir(exist_ok=True)
    (target/'run.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    (target/'evidence.md').write_text(evidence(rows))
    print(json.dumps({'cases':len(rows),'main_status':rows[0]['status'],
                      'main_minima':len(rows[0]['intervention_all_minima'])}))

if __name__ == '__main__':
    main()
