# Research question

> **With the same clinical text and model budget, do explicit de-identification instructions miss fewer sensitive entities than general instructions, while keeping non-sensitive content intact?**

**Why it matters:** A missed entity can expose personal information, while over-deletion destroys the text's research value. A single overall score cannot show the cost of either error.

**Central tension:** More detailed rules may raise coverage, but they may also delete ordinary words or change the meaning; rare names and contextual ambiguity let an average hide the weak spots.

**Current evidence and gap:** [README.md](README.md) lists the explicit, implicit and general prompts and the 2023 comparison across several models, but entity definitions, data splits and scoring need to be unified before the differences can be interpreted.

**Smallest decisive experiment:** On annotated text whose use is licensed, freeze a document-level split, the model revisions and the generation settings, and compare a rule-based baseline with each prompt. Report entity-level recall, over-deletion, text fidelity and failures separately, and test controlled perturbations such as name substitution. Never spread variants of the same source text across training and test. If a gain comes from over-deletion or data leakage, reject the hypothesis.

This is a proposed evaluation, not an anonymisation guarantee; no original sensitive text is reproduced.

中文版：[PROBLEM.zh.md](PROBLEM.zh.md)
