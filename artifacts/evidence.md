# Exact finite-catalogue evidence

Synthetic operation names only. No model, API, token or action ran. Counts enumerate designed catalogues, not sampled attacks.

| Scenario | Scope subsets | Sufficient grants | Distinct sufficient footprints | Minimal footprints | Status |
|---|---:|---:|---:|---:|---|
| tradeoff | 4 | 3 | 3 | 2 | incomparable_minima |
| exact_task_scope | 8 | 7 | 4 | 1 | unique_least |
| aliases | 8 | 7 | 3 | 2 | incomparable_minima |
| scope_names_are_not_authority | 8 | 5 | 2 | 1 | unique_least |
| equal_metrics_different_operations | 4 | 3 | 3 | 2 | incomparable_minima |
| risk_dominance_not_containment | 4 | 3 | 3 | 2 | incomparable_minima |
| infeasible | 2 | 0 | 0 | 0 | infeasible |
| empty_task | 4 | 4 | 4 | 1 | unique_least |

## tradeoff

Task: ['summary.read']

Control shows: {'grant': ['project_editor'], 'footprint': ['project.edit', 'summary.read'], 'extras': ['project.edit'], 'risk': {'operations': 2, 'writes': 1, 'services': 1, 'admin': 0}}

| Grant | Footprint | Extra operations | Operations / writes / services / admin |
|---|---|---|---|
| organization_reader | billing.read, directory.read, summary.read | billing.read, directory.read | 3 / 0 / 3 / 0 |
| project_editor | project.edit, summary.read | project.edit | 2 / 1 / 1 / 0 |

Declared-preference ties are preserved: {"admin": [["organization_reader"], ["project_editor"]], "operations": [["project_editor"]], "services": [["project_editor"]], "writes": [["organization_reader"]]}

Exclusive-operation witnesses: [{"left": ["organization_reader"], "left_only": ["billing.read", "directory.read"], "right": ["project_editor"], "right_only": ["project.edit"]}]

Risk-vector dominated minima (not footprint containment): []

## exact_task_scope

Task: ['summary.read']

Control shows: {'grant': ['summary_only'], 'footprint': ['summary.read'], 'extras': [], 'risk': {'operations': 1, 'writes': 0, 'services': 1, 'admin': 0}}

| Grant | Footprint | Extra operations | Operations / writes / services / admin |
|---|---|---|---|
| summary_only | summary.read | (none) | 1 / 0 / 1 / 0 |

Declared-preference ties are preserved: {"admin": [["summary_only"]], "operations": [["summary_only"]], "services": [["summary_only"]], "writes": [["summary_only"]]}

Exclusive-operation witnesses: []

Risk-vector dominated minima (not footprint containment): []

## aliases

Task: ['summary.read']

Control shows: {'grant': ['project_editor'], 'footprint': ['project.edit', 'summary.read'], 'extras': ['project.edit'], 'risk': {'operations': 2, 'writes': 1, 'services': 1, 'admin': 0}}

| Grant | Footprint | Extra operations | Operations / writes / services / admin |
|---|---|---|---|
| organization_reader | billing.read, directory.read, summary.read | billing.read, directory.read | 3 / 0 / 3 / 0 |
| project_editor | project.edit, summary.read | project.edit | 2 / 1 / 1 / 0 |

Declared-preference ties are preserved: {"admin": [["organization_reader"], ["project_editor"]], "operations": [["project_editor"]], "services": [["project_editor"]], "writes": [["organization_reader"]]}

Exclusive-operation witnesses: [{"left": ["organization_reader"], "left_only": ["billing.read", "directory.read"], "right": ["project_editor"], "right_only": ["project.edit"]}]

Risk-vector dominated minima (not footprint containment): []

## scope_names_are_not_authority

Task: ['directory.read', 'summary.read']

Control shows: {'grant': ['read_directory', 'read_summary'], 'footprint': ['directory.read', 'summary.read'], 'extras': [], 'risk': {'operations': 2, 'writes': 0, 'services': 2, 'admin': 0}}

| Grant | Footprint | Extra operations | Operations / writes / services / admin |
|---|---|---|---|
| read_directory, read_summary | directory.read, summary.read | (none) | 2 / 0 / 2 / 0 |

Declared-preference ties are preserved: {"admin": [["read_directory", "read_summary"]], "operations": [["read_directory", "read_summary"]], "services": [["read_directory", "read_summary"]], "writes": [["read_directory", "read_summary"]]}

Exclusive-operation witnesses: []

Risk-vector dominated minima (not footprint containment): []

## equal_metrics_different_operations

Task: ['summary.read']

Control shows: {'grant': ['left'], 'footprint': ['directory.read', 'summary.read'], 'extras': ['directory.read'], 'risk': {'operations': 2, 'writes': 0, 'services': 2, 'admin': 0}}

| Grant | Footprint | Extra operations | Operations / writes / services / admin |
|---|---|---|---|
| right | billing.read, summary.read | billing.read | 2 / 0 / 2 / 0 |
| left | directory.read, summary.read | directory.read | 2 / 0 / 2 / 0 |

Declared-preference ties are preserved: {"admin": [["right"], ["left"]], "operations": [["right"], ["left"]], "services": [["right"], ["left"]], "writes": [["right"], ["left"]]}

Exclusive-operation witnesses: [{"left": ["right"], "left_only": ["billing.read"], "right": ["left"], "right_only": ["directory.read"]}]

Risk-vector dominated minima (not footprint containment): []

## risk_dominance_not_containment

Task: ['summary.read']

Control shows: {'grant': ['left'], 'footprint': ['directory.read', 'summary.read'], 'extras': ['directory.read'], 'risk': {'operations': 2, 'writes': 0, 'services': 2, 'admin': 0}}

| Grant | Footprint | Extra operations | Operations / writes / services / admin |
|---|---|---|---|
| right | billing.read, project.edit, summary.read | billing.read, project.edit | 3 / 1 / 2 / 0 |
| left | directory.read, summary.read | directory.read | 2 / 0 / 2 / 0 |

Declared-preference ties are preserved: {"admin": [["right"], ["left"]], "operations": [["left"]], "services": [["right"], ["left"]], "writes": [["left"]]}

Exclusive-operation witnesses: [{"left": ["right"], "left_only": ["billing.read", "project.edit"], "right": ["left"], "right_only": ["directory.read"]}]

Risk-vector dominated minima (not footprint containment): [{"by": ["left"], "grant": ["right"]}]

## infeasible

Task: ['billing.read']

Control shows: None

| Grant | Footprint | Extra operations | Operations / writes / services / admin |
|---|---|---|---|

Declared-preference ties are preserved: {"admin": [], "operations": [], "services": [], "writes": []}

Exclusive-operation witnesses: []

Risk-vector dominated minima (not footprint containment): []

## empty_task

Task: []

Control shows: {'grant': [], 'footprint': [], 'extras': [], 'risk': {'operations': 0, 'writes': 0, 'services': 0, 'admin': 0}}

| Grant | Footprint | Extra operations | Operations / writes / services / admin |
|---|---|---|---|
| (empty) | (empty) | (none) | 0 / 0 / 0 / 0 |

Declared-preference ties are preserved: {"admin": [[]], "operations": [[]], "services": [[]], "writes": [[]]}

Exclusive-operation witnesses: []

Risk-vector dominated minima (not footprint containment): []
