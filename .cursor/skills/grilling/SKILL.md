---
name: grilling
description: >-
  One-question-at-a-time interview loop for plans and designs. Loaded by
  grill-me and grill-with-docs; not invoked directly.
disable-model-invocation: true
---

Interview the user relentlessly about every aspect of this plan until shared understanding is reached. Walk each branch of the design tree; resolve dependencies between decisions one at a time. For each question, give your recommended answer.

Ask **one question at a time** and wait for feedback before the next. Multiple questions at once is bewildering.

If a question can be answered from the codebase, explore the codebase instead of asking.

## Done when

Scope, boundaries, trade-offs, and open risks are aligned. End with a short bullet summary of decisions and remaining unknowns.

## Handoff

If the user wants terms or decisions persisted, suggest `@grill-with-docs` or `@domain-modeling`.
