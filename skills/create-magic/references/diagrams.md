# The two diagrams (context)

Read this when he asks where a stage sits in the pipeline, or when you need to explain the whole path.

**Validation pipeline (layer 1).** Proves that the audience has the problem.
Vision + Target audience (starting assumptions) → Desired outcomes → 1. Choose desire to validate → 2. Hypotheses + bar → 3. Choose how to validate → 4. Validate (validation profile, then the evidence log) → 5. Result + decision → Share → Gate → pass: Validated opportunity, the start of layer 2. Not yet or fail: next lap.

**Solution validation (layer 2).** Used after the outcomes are validated.
Validated opportunity → Explore solutions → Pick one way → Hypotheses + bar → Choose how to validate → Minimal requirements → Build → Validate → Document + decide → Share → Next lap or layer.

Source files: GitHub repo `bodya-pipeline`, folder `diagrams/`. `pipeline.html` is a tab shell: the first tab shows the combined diagram (`diagrams/pipeline/`: both layers in one Archify workflow, with a "Bridge" lane that holds the Validated opportunity). The "+" opens a project tab: its `0 Plan` checklist on the left and its steps column on the right. A project's diagram, steps and plan are written by `scripts/build_project_diagram.py` from the project's notes in the vault. The separate `idea-validation` and `solution-validation` diagrams are still there.

**This version of the skill covers all of layer 1, up to and including the gate.** Layer 2 is context only.
