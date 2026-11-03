---
title: "Two agents can both claim a task and only one claim survives"
date: 2026-10-25
tags: [agents, coordination, mcp, testing]
source: https://github.com/dan-calin/shared-agent-memory
---

# Two agents can both claim a task and only one claim survives

I tested shared-agent-memory 0.7.0 (commit `29e96c663a43da557c25132c4d569bce9d9e6b12`) with invented data, checked on 2026-10-24.

The board writes its file through an atomic rename. That stops a half-written file. It does not stop two writers from reading the same old file, each adding a claim, and each renaming its own copy into place. In the test, two processes called `board.claim` at the same time. Both returned normally. The board kept one claim.

Results against the behaviour I wanted from a coordination layer:

- Board fixtures: 8 of 12 expectations met.
- Memory-tool fixtures: 8 of 11 expectations met.
- Symlink aliases and missing session IDs got past the conflict checks.
- Claims with future timestamps stayed live.
- A search for one project name matched three projects. An empty search returned the whole invented graph.

Some of this is by design. The README describes claims as advisory and sharing as a naming convention, and the memory server says it has no model for resolving conflicting beliefs. Names are a retrieval convention, not an access boundary.

## Evidence

The recorded results are public in [agent-claims](https://github.com/maxmorrish/agent-claims/tree/67d8a73/evidence/20261024-shared-memory) (23 claims, 16 expectations met). They are archived results: the runnable fixture is not published yet, so they can be read but not rerun. A green rerun would not mean the package passed, since the recorded outcome includes the known failures.

## Not verified

No live agents, no production setup and no private data. A separate file-lock adapter was tested on its own and is not covered here.
