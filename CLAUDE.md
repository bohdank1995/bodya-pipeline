# bodya-pipeline: notes for Claude

- This repo holds reusable experiment pipelines (`pipelines/`) and the experiments run with them (`projects/`). The method is in `docs/method.md`.
- Every experiment must name its profit lever and set a success bar before it starts.
- New experiment: copy the pipeline's `templates/` into `projects/<project>/<milestone>/<NNN-slug>/`. Don't edit the templates themselves for one experiment.
- Diagrams use the Archify skill. Keep each diagram in `diagrams/<name>/`, with `candidate.json` as the source and the rendered `.html` beside it. Set `meta.output` to that folder. Don't commit Archify receipts (they're gitignored).
