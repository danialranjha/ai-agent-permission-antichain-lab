# AI-agent permission alternatives lab

A minimal permission grant need not be the only minimal choice. This independent, synthetic experiment enumerates all available scope combinations for a fixed task and shows the different extra actions allowed by competing minimal grants.

No model, vendor API, token, browser, or actual operation runs. The catalogue and operation names are invented. This is a mathematical audit of permission choices, not a vulnerability report or permission-enforcement system.

## Hypothesis and threat model

A selector can return a minimal sufficient grant while concealing another equally minimal grant with different unwanted reach. Showing all minimal footprints and explicit preference criteria makes that choice inspectable. It does not prove that a human or model will choose better.

Assume an agent requests authority for a known task. The catalogue, task definition and operation metadata remain trusted. The selector may choose undesirable extra authority; no attacker compromise is demonstrated. A footprint is the exact set of operations a grant allows in this finite model. The program never executes those operations.

## Setup and exact commands

Python 3.10+ standard library only. No install, network or credentials are needed.

```sh
python3 -B -m unittest -v
python3 -B experiment.py
```

The second command regenerates [run.json](artifacts/run.json) and [exact evidence](artifacts/evidence.md). Output has no timestamp, random value or machine path. Input is [fixtures.json](fixtures.json); algorithm is [experiment.py](experiment.py).

## Results

Eight designed catalogues were enumerated. Eleven test methods pass, including an independent bitmask oracle covering all 512 catalogues of three scopes over three operations and all eight possible tasks: 4,096 catalogue/task comparisons. These are exhaustive checks of a tiny finite domain, not sampled attacks or a measurement of model decisions.

The main task is to read a project summary. Four scope subsets exist: neither grant, each grant separately, and both together. Three suffice, but only two footprints are minimal.

| Minimal grant | Allowed operations | Extra actions beyond task | Actions | Writes | Services | Admin |
|---|---|---|---:|---:|---:|---:|
| project_editor | summary.read, project.edit | Edit this project | 2 | 1 | 1 | 0 |
| organization_reader | summary.read, directory.read, billing.read | Read directory and billing data | 3 | 0 | 3 | 0 |

Neither footprint contains the other. The combined grant is strictly larger than either. Preferring fewer actions chooses project_editor. Preferring fewer writes chooses organization_reader. Both answers are well-defined under their declared metric; neither is the least footprint under containment.

- **Single-grant view:** Present the minimal grant with fewest operations, using a deterministic name tie-break.
- **Alternatives view:** Present every distinct minimal footprint, exclusive extra actions and the choices tied for each declared metric.

Single-grant view presents project_editor alone. Alternatives view presents both choices and their tradeoff. This changes the information disclosed, not the catalogue, a permission decision, or an executed action.

Adding summary_only, which permits only summary.read, changes the result to a unique least footprint. That counterfactual shows the ambiguity comes from available authority, not from the task being impossible.

## Technical walkthrough

For every subset of available scope names, take the union of its operation sets. Keep sufficient unions containing every required task operation. Equivalent footprints collapse to one representative: fewest scope names, then lexicographic order. Remove any sufficient footprint that strictly contains another sufficient footprint. Remaining footprints are the minimal sufficient alternatives.

When exactly one remains, it is a least footprint in this finite set. Several remaining footprints are mutually incomparable. No remaining footprint means infeasible. An empty task has the empty footprint as its least choice.

The four displayed measures are operation count, count of explicitly write-marked operations, distinct service count and a binary any-admin flag. These are declared metadata summaries, not universal risk scores. Each preference returns every tied minimal alternative. The limited control's lexicographic tie-break is deliberately explicit, not claimed to reflect security.

The additional fixtures isolate common mistakes:

- Identical footprints with different names collapse; equivalent authority is not incomparability.
- One broad scope can be strictly worse than a pair of narrow scopes. Name-set inclusion or the number of scope names does not measure authority.
- Two different extra operations can have equal values on every displayed measure. Equal metrics do not make the footprints equal.
- One minimal footprint can be worse on the displayed risk vector while still incomparable by containment. Risk-vector dominance does not remove a footprint from the containment-minimal set.
- An infeasible task stays infeasible. An empty task needs no grant.

Exact per-case sets, counts and exclusive-operation witnesses are in [evidence.md](artifacts/evidence.md). Tests also permute scope order and reject unknown operations, malformed metadata and catalogues above the 12-scope bound. Oversized input fails explicitly; the program does not present a partial enumeration as complete.

## Source and interpretation

[Incomparable Minima in Agent Tool Authorization](https://arxiv.org/html/2610.31914v1), sections 3 and 13, motivates comparing effective operation sets and exposing competing minimal grants. This lab independently constructs a small fictional catalogue. It does not copy the paper's datasets or code, reproduce its vendor-table percentages, or run its model-choice study.

## Limits and supported engineering check

Complete enumeration grows exponentially; the 12-scope limit is deliberate. Results depend entirely on correct operation mappings and task requirements. Real resource-level conditions, scope dependencies, baseline permissions, deny rules, token lifetimes, runtime enforcement and changing catalogues are absent. The service/write/admin labels are stipulated, not inferred from HTTP verbs. The test does not establish user comprehension, better model choices, reduced attacks or production least privilege.

For a small, trusted catalogue, enumerate distinct minimal sufficient operation sets before presenting a permission choice. If several remain, show their different extra actions and state the preference used to choose. Verify that any displayed unique least result survives equivalent-name, combined-scope and missing-task controls. Do not describe a metric-preferred grant as universally least authority.
