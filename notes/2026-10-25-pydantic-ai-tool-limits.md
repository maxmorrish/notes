---
title: "Pydantic AI's tool_calls_limit counts successes, not attempts"
date: 2026-10-25
tags: [agents, pydantic-ai, retries, testing]
source: https://github.com/pydantic/pydantic-ai/releases/tag/v2.59.0
---

# Pydantic AI's tool_calls_limit counts successes, not attempts

I tested pydantic-ai-slim 2.59.0 on 2026-10-24 with a 28-assertion fixture. FunctionModel drove the real agent loop with a scripted function in place of a model. Real model requests were off and socket connections were blocked. Each tool call appended a made-up integer to a list, so every effect could be counted.

All 28 expectations held. These are documented behaviours, not bugs:

- Missing, negative, coercible and extra arguments were rejected before the tool body ran. A corrected retry produced one effect.
- When validation retries ran out, the run stopped after two model-function calls with no tool effect.
- A plain `RuntimeError` stopped the run after one callback.
- A batch of two tools against a budget of one success was rejected before either callback ran.
- With `tool_calls_limit=1`, three `ToolFailed` callbacks still ran. Only `request_limit=3` bounded them, because the tool-call limit counts successful calls.
- `ModelRetry` raised after an effect produced the effect twice, unless the sink deduplicated on a stable operation key.

The practical point: a successful-call limit does not cap failed attempts. If a tool has side effects, give each operation a stable key and deduplicate on it.

## Reproduce

From the fixture folder:

```sh
sh setup.sh && sh verify.sh
```

Dependencies are pinned in `requirements.lock`. The fixture files are not published with this note yet.

## Not verified

No real model, background tools, streaming, cancellation, persistence or production permission checks. Issue [10109](https://github.com/pydantic/pydantic-ai/issues/10109) covers retry accounting for background tools, which this fixture does not exercise.
