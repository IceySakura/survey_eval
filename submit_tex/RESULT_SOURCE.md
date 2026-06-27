# Survey Summary Table Source

This table corresponds to the `eval_survey_new` result group:

- Source CSV: `../eval_survey_new/eval/results/eval_survey_new_scores.csv`
- Source summary: `../eval_survey_new/eval/results/eval_survey_new_analysis.md`
- Per-task JSON/Markdown reports: `../eval_survey_new/eval/results/eval_result_*_20260327_*.json` and `../eval_survey_new/eval/results/eval_report_*_20260327_*.md`
- Generated TeX source root: `../eval_survey_new/sources`, which is a symlink to `../eval-survey/sources`
- Organized experiment TeX files: `experiments/<task>/<agent>_<backbone>/related_works.tex`
- Experiment manifest: `experiments_manifest.csv`

Task macro mapping in `survey_summary_table.tex`:

- `\Paperone` = `sfedavg`
- `\Papertwo` = `subspacescaffold`
- `\Paperthree` = `sudamuon`

Evaluation-model label mapping:

- `gpt51` = `GPT-5.1`
- `sonnet4.6` = `Sonnet 4.6`
- `dpsk` = `DeepSeek-v3.2`

Generation-backbone label mapping:

- `dpsk` = `DeepSeek-v3.2`
- `gpt51` = `GPT-5.1`
- `gpt54` = `GPT-5.4`
- `sonnet4.6` = `Sonnet 4.6`

Each cell reports `total = dim1 + dim2`, where `dim1` is content accuracy and `dim2` is citation relevance, both from `eval_survey_new_scores.csv`.
