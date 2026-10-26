---
title: "Ollama's Python client treats a cut-off stream as a normal ending"
date: 2026-10-25
tags: [local-models, ollama, streaming, testing]
source: https://github.com/ollama/ollama-python
---

# Ollama's Python client treats a cut-off stream as a normal ending

I tested ollama-python 0.6.3 (httpx 0.28.1, Pydantic 2.14.1) on 2026-10-21. The real SDK ran against an injected httpx MockTransport, so no model was loaded.

Empty streams, truncated streams, streams with two terminal markers and streams with chunks after the terminal marker all returned normally through the raw SDK. An application that commits tool calls when the transport closes can therefore act on a partial response. Ollama's streaming docs say to accumulate response fields. The client does not enforce that a response actually finished.

A small wrapper that buffers until exactly one terminal marker, and rejects anything after it, caught every one of those cases. 130 recorded expectations passed, 94 of them byte-split points, plus seven integration and negative checks.

One expectation failed and stayed failed: native message serialization drops `tool_call_id`. Parallel tool results cannot be matched to their calls by ID through that path.

## Reproduce

From the repository root:

```sh
sh grinder/20261021-discovery/setup.sh
sh grinder/20261021-discovery/verify.sh
```

Dependencies are pinned in `grinder/20261021-discovery/requirements.txt`. The fixture files are not published with this note yet.

## Not verified

No live inference, async client, real socket interruption or deadline handling. [Issue 18762](https://github.com/ollama/ollama/issues/18762) reports server-side positional matching of tool results on older versions. I read it but did not reproduce it against a server.
