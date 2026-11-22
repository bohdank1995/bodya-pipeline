# Plan checklist: `0 Plan.md`

After each stage, rewrite `0 Plan.md` as the checklist for the stage that comes next. The note holds only this checklist. Nothing else.

## Format

- `# Plan`, then groups of tasks. A group has a heading that links to the note it belongs to: `### [[3 Choose how to validate|Workaround hunting]]`. A stage with one list of tasks has no heading.
- A task is `- [ ] text`. Write it in plain words that still make sense in a week: start with a verb, say what to do, one action each. Do not use words like "run" or "execute".
- Keep ticks. A task with the same text stays ticked. Drop the tasks of earlier stages.
- Keep items he added by hand. Put them under `### Mine`.

## Validate stage: built from the methods table

Read `4 Validation/3 Choose how to validate.md`.

- **A group for each method without people.** Heading: the method's name, linking to `3 Choose how to validate`. Tasks: "Prepare: [its Needs, in lower case]" (skip it when the Needs says "the same ...", "Nothing extra", or repeats an earlier one), then the first sentence of its first "How". Add "Do it for [Sample]" when the Sample starts with a number.
- **One group for the methods with people.** Heading: their names joined with " + ". Tasks: "Book conversations with [Sample]", then the first sentence of each method's "How". Drop a label before a colon, as in "Last part of the same conversation: ask them ...".
- **A last group, "Evidence log"**, linking to `5 Evidence log`. Tasks: "Log each public-source finding in [[5 Evidence log#From public sources]] within 24 hours" when a method has no people, and "Log each conversation in [[5 Evidence log#From people]] within 24 hours" when a method has people.

## Other stages

| Stage | Tasks |
|---|---|
| 1. Vision | Answer the vision questions with Claude. Pick one version. Save it as [[1 Vision]] |
| 2. Target audience | Answer the audience questions with Claude. Write the audience statement. Fill in the fields in [[2 Target Audience]] |
| 3. Desired outcomes | List the outcomes people want. Sort them and write the chain. Save it as [[3 Desired Outcomes]] |
| 4. Choose desire to validate | Pick one outcome from [[3 Desired Outcomes]]. Write the claim in [[1 Choose desire to validate]] |
| 5. Hypotheses + bar | Write 3 to 5 hypotheses in [[2 Hypotheses and bar]]. Give each one a success bar with a number. Write the rule for the whole claim |
| 6. Choose how to validate | Choose a method for each hypothesis in [[3 Choose how to validate]]. Write the next steps |
| 8. Result + decision | Count the people for and against each hypothesis in [[6 Result and decision]]. Compare with the success bars and the verdict rule. Decide: keep, narrow, change or stop. Write what you learned and the next step |
| Share | Write the post or the portfolio case in [[7 Share]] |
| 9. Gate | Run the six checks in [[8 Gate]]. If it passes, write [[5 Validated opportunity]] |

## The script

If the `bodya-pipeline` repo is reachable, this command writes the note and the data for the project's tab in one go (`--plan-only` skips the diagram):

`python3 scripts/build_project_diagram.py <slug> --vault <project folder> --title <name> --plan-only`
