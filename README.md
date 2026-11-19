# Unreported: a maintenance benchmark for coding agents

29 real bugs from SWE-bench Verified, each hidden among other signals a maintainer would see:
two silent defects nobody reported, and traps that should be left alone. The question it asks is
not "can an agent fix the bug it is handed" but **can an agent find what was never reported, tell
real problems from noise, and fix them without side effects.**

Write-up and results: https://hibonzai.com/bench

This repository holds everything needed to check the numbers: the tasks and answer key, how the
hidden defects were made, the judge, and the per-trial records of every published run.

## What is here

| Path | What it holds |
|---|---|
| `tasks/<repo>__<name>-<n>/` | One task: `instruction.md` (exactly what a system is told, with its 7 signals), `tests/` (the SWE-bench verifier, the hidden-defect tests in `tests/hidden/`, the decoy checks in `tests/decoys/`), `environment/` (the task's image) and `solution/` (SWE-bench's reference fix for the reported bug) |
| `truth.json` | The answer key: which signal in each task is the reported bug, a hidden defect, an already-fixed issue, the outage log or a won't-fix issue |
| `hidden/` | The 58 hidden defects: the patch that introduces each, its test, the weak production trace it produces, and a one-line summary. `gen_hidden.py` is the generator and its three acceptance checks |
| `build_factory.py` | Builds the tasks from SWE-bench Verified |
| `judge/` | `judge.py` (the pull request rubric and prompt, and how results are scored), `reference/` (the reference diffs the judge compares against), `regrade/` (local re-grading of SWE-bench test logs) |
| `results/` | One file per published run with every trial's scores, and `summary.json` with the numbers on the page |
| `runs/<system>/` | Per-trial records: the grade, the verifier's outputs, each system's triage decisions and pull request descriptions and diffs, and Claude Code's full transcripts |

## The systems

| Folder | System | Model |
|---|---|---|
| `claude-code-opus-5.5`, `claude-code-sonnet-5.5` | Claude Code 2.1.325 | Claude Opus 5.5, Claude Sonnet 5.5 |
| `bonzai-opus-5.5`, `bonzai-sonnet-5.5` | Bonzai Self-Driving | Opus 5.5 investigates and Sonnet 5.5 fixes; Sonnet 5.5 throughout |
| `bonzai-*-pr-replay` | The fix step re-run on each Bonzai run's saved investigations, so each pull request's own diff is recorded | as above |

Every model ran at high reasoning effort, one run per system, on identical 8 vCPU / 16 GB VMs.

## What is not here

Bonzai's own prompts and its conversation threads are product code and are not published. For
Bonzai trials each session's final report and cost totals are kept. Claude Code's transcripts are
whole; its only prompt is the task's `instruction.md`.

## Re-running

`judge/judge.py` documents its arguments. Scoring a run needs the trial folders under `runs/`, the
answer key and the reference diffs: `python3 judge/judge.py truth.json judge/reference out.json <trial job dirs>`.
Running the systems again needs Harbor and the task images; the harness that launches them is in
https://github.com/Developing-Gamer/bonzai-benchmarks (private).

## Licenses

Our additions (the hidden defects, answer key, signals and scripts) are released under CC BY 4.0.
The underlying task repositories and issue text come from SWE-bench Verified and the open-source
projects it samples (astropy, django, matplotlib, seaborn, flask, requests, xarray, pylint, pytest,
scikit-learn, sphinx, sympy) and keep their own licenses.

## Contamination

The answer key and hidden tests are public, so a system trained on this repository would score
well on these 29 tasks. Treat results from systems that could have seen it as unverified.

## Citation

```
@misc{jain2026unreported,
  title  = {Unreported: a maintenance benchmark for coding agents},
  author = {Armaan Jain},
  year   = {2026},
  url    = {https://hibonzai.com/bench},
}
```
