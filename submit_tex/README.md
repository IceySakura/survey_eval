# Survey Eval Submit TeX

This folder contains the TeX artifacts corresponding to the survey-evaluation table.

## Table

- `survey_summary_table.tex`: table snippet for `\input{...}` into the paper.
- `main.tex`: standalone wrapper for checking the table in isolation.

## Experiment TeX Files

The table evaluates 24 generated related-work submissions:

- 3 tasks: `sfedavg`, `subspacescaffold`, `sudamuon`
- 4 generation backbones: `dpsk`, `gpt51`, `gpt54`, `sonnet4.6`
- 2 agents: `base`, `reasflow`

The corresponding TeX files are organized as:

```text
experiments/<task>/<agent>_<backbone>/related_works.tex
experiments/<task>/<agent>_<backbone>/references.bib
```

Each task directory also includes its `survey_plan.md`.

Use `experiments_manifest.csv` to map each table row/variant back to its source under `../eval-survey/sources`.
