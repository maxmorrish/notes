---
title: "A successful capture does not prove redaction"
date: 2026-11-08
tags: [agents, memory, redaction, testing]
source: https://github.com/tigerless-labs/agent-memory
---

# A successful capture does not prove redaction

tigerless-labs/agent-memory runs a shared redactor before it archives a capture and builds the distillation instruction. A recent fix taught it to handle quoted credential values. I tested the real capture path with invented canary strings to see what still gets through.

At commit `2da5a42`, 13 of 31 redaction and control cases match expectations, against 6 of 31 at `75531cd` before the fix. In the other 18 current cases, canary fragments survive in the archive, the returned increment and the distillation instruction. The pattern is consistent: quoted values containing spaces, commas or quotes fall outside the regex's simple value grammar, so they are missed or only partly replaced. Bare provider-style keys of the supported shapes are removed.

Every second capture of the same content returned an empty increment. Deduplication works, and it works the same whether or not the first capture was cleaned, so a clean dedup result says nothing about redaction.

## Evidence

Python 3.12, unmodified core and adapters, two commits compared. The 31 cases cover two credential field names, four value shapes, three text formats, five bare shapes and two negative controls. They are a tailored matrix, not an estimate of real-world recall. Relevant upstream work: [PR 117](https://github.com/tigerless-labs/agent-memory/pull/117) and [PR 118](https://github.com/tigerless-labs/agent-memory/pull/118). The runnable fixture is not published yet.

## Not verified

Real credentials, other token formats, malformed encodings, model inference, host hooks, and whether anything reaches the network. Only synthetic content was used.
