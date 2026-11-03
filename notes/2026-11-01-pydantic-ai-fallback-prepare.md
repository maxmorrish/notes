---
title: "Sticky fallback preparation is not one-to-one with model calls"
date: 2026-11-01
tags: [agents, pydantic-ai, fallback, cost-tracking, testing]
source: https://github.com/pydantic/pydantic-ai/pull/11330
---

# Sticky fallback preparation is not one-to-one with model calls

I tested `ModelFallback` in Pydantic AI 2.64.0 on 16 synthetic cases and 112 checks. 108 passed. All 16 checks each for call order, output, model identity, model-specific settings, failed attempts and once-per-run behaviour held.

The four misses are one behaviour. A sticky routing decision lives inside per-attempt preparation, so preparation can repeat before any request goes out. In four sticky continuation cases, preparation ran for the primary model and then the backup, while only the backup received a request.

If a hook counts preparations as provider calls, its count runs high. Keep routing preparation pure and idempotent, and don't charge cost or trigger external effects from `prepare_model_request`. This is an integration caveat from how the feature is built. It is not an established upstream bug.

## Reproduce

The fixture for this note is not public yet. It will be added to [agent-claims](https://github.com/maxmorrish/agent-claims) with a rerun command, and this section will link to it.

## Not verified

Pydantic AI 2.64.0 only, with no earlier version to compare because the API is new. No real providers, billed calls, native token counting or durable workers.
