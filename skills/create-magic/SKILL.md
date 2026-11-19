---
name: "create-magic"
description: "Run when Bodya says \"let's create magic\", starts a new project, or wants to formulate a vision, a target audience, desired outcomes, what to validate, hypotheses with success bars, or to run the validation and the gate. Guides one project through his validation pipeline step by step, using the notes in My Brain/Rules and templates, and saves each result as a note in the project folder. Covers all of layer 1, from the vision to the gate."
---

# Create magic

Guides one project through the first part of Bodya's validation pipeline (layer 1). It finds which stage the project is at, asks the questions for that stage, formulates his answers with the rules and templates he built, and saves the result.

Trigger: "let's create magic", "I'm starting a project", or a request to work on one of the stages below. If he names a project, use only that project. If the name matches more than one folder, ask which.

This file holds the working rules and the stage finder. Each stage's steps are in a file under `references/`. Read the file for the stage before starting it. For the two diagrams as context, read `references/diagrams.md`.

## Where things live

Vault root: `My Brain/`.

Rules and templates, in `My Brain/Rules and templates/`: `Vision statement rules`, `Vision questions`, `Target audience rules`, `Target audience questions`, `Desired outcomes rules`, `Choose what to validate rules`, `Hypothesis rules`, `Choose how to validate rules`, `Validation profile rules`, `Evidence log rules`, `Result and decision rules`, `Gate rules`.

Project notes, in `My Brain/<Project>/`: `Vision.md`, `Target Audience.md`, `Desired Outcomes.md`, `Validation Plan.md`, `Evidence Log.md`.

Before each stage, read that stage's notes again. Do not work from memory of the rules. If a rules note is missing, say so and ask what to do.

## Find the stage

Read the project folder. Take the first row that matches, then read the reference file in the last column.

| State of the project folder | Stage | Reference |
|---|---|---|
| No `Vision.md`, or it is empty | 1. Vision | `foundation.md` |
| `Vision.md` exists, no `Target Audience.md` | 2. Target audience | `foundation.md` |
| Audience exists, no `Desired Outcomes.md` | 3. Desired outcomes | `foundation.md` |
| Outcomes exist, no `Validation Plan.md`, or the last entry has no "What we validate" | 4. Choose what to validate | `plan-the-test.md` |
| The last entry has "What we validate" but no hypotheses table | 5. Hypotheses + bar | `plan-the-test.md` |
| The last entry has a hypotheses table but no methods table | 6. Choose how to validate | `plan-the-test.md` |
| The last entry has a methods table but no next steps table | 6, part 2: next steps | `plan-the-test.md` |
| The last entry has a next steps table but no validation profile | 7, part 1: validation profile | `validate-and-gate.md` |
| The profile exists, and `Evidence Log.md` has fewer people than the sample size for this entry | 7, part 2: evidence log | `validate-and-gate.md` |
| The evidence log reaches the sample size, and "Result and decision" is empty | 8. Result + decision | `validate-and-gate.md` |
| The result is written, and the gate has not run | 9. Gate | `validate-and-gate.md` |
| The gate result is "Pass" | Stop. Layer 2 is not built yet | |
| The gate result is "Not yet" | Back to stage 7, part 2, for more evidence | `validate-and-gate.md` |
| The gate result is "Fail" | A new entry, starting at stage 4 | `plan-the-test.md` |

If he asks for the result before the sample size is reached, do stage 8 and use "Not enough data" where the rules say so.

If he says he is starting a project, begin at stage 1. If he names a stage whose earlier stage is missing, say what is missing and offer to do it first.

Say the stage in one line.

## Ask before every stage

Before starting any stage, including the first one, ask one yes or no question that names it, and wait for his answer. For example: "Should we now choose how to validate?" Do not start the stage until he says yes. Ask again before part 2 of a stage.

## Chat first, file second

Show everything in the chat: the options, the drafts, the questions and the tables. Write to the project file only the result he agreed to, after his OK. Show every table in the chat even though the same table is also saved in Obsidian.

## How to work every stage

- Ask **one question at a time**.
- Every question can be answered with **"unknown"**. Record it as an assumption. Never fill it with a guess.
- Do not suggest answers. Give examples only if he asks.
- If he says he does not understand, rephrase the question with his earlier answers filled in.
- If he gives more than one answer to a question that asks for one, record all of them.
- Each question has one idea, states its scope, can be answered from what he knows, and has options that do not overlap.
- Use his own words. Do not add items he did not give. If you think something is missing, ask.
- When the draft is ready, check it against the stage's rules, show it, and let him correct it.
- Before writing, say which file will change and wait for his OK.

## After each stage

Show one progress line, then the next step:

`Vision ✓ → Audience ✓ → Outcomes ✓ → Choose what ✓ → Hypotheses + bar ✓ → Choose how ✓ → Validate ✓ → Result ✓ → Gate ✓ → Layer 2 (not built yet)`

## Not built yet

Layer 2 (solution validation), the X post and the portfolio page. When the gate passes, say that this version stops here, and leave the plan as it is.

## Rules

- Say which files will change and wait for his OK before writing anything.
- Change only the stage's own file, `Validation Plan.md` and `Evidence Log.md`.
- Never invent facts, numbers or quotes. Unknown stays unknown.
- Keep prose plain: no inflated words, no rule-of-three padding, no em dashes.
- Keep answers short. He is easily overwhelmed, so show one stage at a time.
- If the vault cannot be reached, say so and tell him to open the Claude desktop app on his Mac and add the My Brain folder from the + menu. Continue by asking for the content and giving him the text to paste.
