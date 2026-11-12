---
title: "A stale resume answer should not answer the next question"
date: 2026-11-08
tags: [agents, langgraph, human-in-the-loop, testing]
source: https://github.com/langchain-ai/langgraph/releases/tag/1.2.20
---

# A stale resume answer should not answer the next question

LangGraph 1.2.20 adds two things for graphs that pause and ask a person something: an opt-in strict resume check, and distinct IDs for successive interrupts inside one task. I tested whether an old answer gets rejected before it changes graph state, and whether legitimate empty, false and null answers still go through.

The synthetic suite runs 198 checks per version. LangGraph 1.2.20 passes 198 of 198; 1.2.19 passes 90 of 198. The checks cover the memory and SQLite checkpointers across three durability modes, plus async in-memory calls. A separate caller that passes interrupt IDs explicitly passed 22 of 22, and eight more observations covered replay, retry and nested graphs. Four saved outputs matched byte for byte in freshly built pinned environments.

Three details matter if you build on this. Strict mode is off unless you set `configurable.__pregel_strict_resume`. A plain dictionary with non-hex keys is still treated as one answer, not a malformed ID map. Replaying a historical checkpoint is deliberately exempt. The checkpoint ID can also stay the same between two questions, so a UI that wants a consistency token should include the pending interrupt IDs in it.

## Evidence

Versions: LangGraph 1.2.20 and 1.2.19, langgraph-checkpoint-sqlite 3.1.3, Python 3.13.9. Upstream changes: [strict resume, PR 9574](https://github.com/langchain-ai/langgraph/pull/9574) and [distinct interrupt IDs, PR 9589](https://github.com/langchain-ai/langgraph/pull/9589). The runnable fixture is not published yet, so the numbers can be read here but not rerun.

## Not verified

Remote enforcement, concurrent processes, async SQLite, live authorization, side effects outside the graph, and production rollout. This shows the library can reject a stale answer when asked to; it does not show that any installed agent turns strict mode on.
