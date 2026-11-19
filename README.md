# bodya-pipeline

Reusable pipelines for running **experiments** across all my projects.
Every experiment has to move its project toward **profit**, and every one ends in something
I can share on X and on my portfolio.

## How it works

Each pipeline is a small Build → Measure → Learn loop (Lean Startup), set up for one kind of question:

```
Hypothesis → Build the smallest test → Measure → Learn → Decide → Share
                                                  │
                         keep going ◄─────────────┴─────────────► change direction
```

- **North star:** profit. Each experiment names the profit lever it pulls (traffic, conversion, price, retention, cost).
- **Evidence ladder:** what people *say* < what they *do* < what they *pay*. Prefer the strongest evidence you can get cheaply.
- **Every lap ends in a decision**, written down in a Learning Card.
- **Sharing is built in.** Each stage leaves material for an X post or a portfolio case study.

See [docs/method.md](docs/method.md) for the full method and the sources it draws on.

## Pipelines

| Pipeline | Answers | Status |
|---|---|---|
| [Problem validation](pipelines/problem-validation/) | Is this problem real, and worth solving? | Pilot |

## Layout

```
docs/          method and principles shared by every pipeline
pipelines/     one folder per pipeline: stages, decision rules, templates
projects/      experiment records, as projects/<project>/<milestone>/<NNN-slug>/
diagrams/      Archify diagrams (candidate.json is the source, .html is the rendered view)
```

## Running an experiment

1. Pick a pipeline.
2. Copy its `templates/` into `projects/<project>/<milestone>/<NNN-slug>/`.
3. Fill the cards as you go. Don't leave them for the end.
4. Write the Learning Card, then the share drafts.
