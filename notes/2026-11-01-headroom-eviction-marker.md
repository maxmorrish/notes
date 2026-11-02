---
title: "A compression cache can outlive its recovery data"
date: 2026-11-01
tags: [agents, context-compression, caching, testing]
source: https://github.com/headroomlabs-ai/headroom/releases/tag/v0.42.0
---

# A compression cache can outlive its recovery data

I tested Headroom 0.42.0 through its public Python `compress` call and direct retrieval from its CCR store, the place it keeps originals so compressed text can be restored. Five synthetic log formats (LF, CRLF, tabs, indentation, blank lines) passed 47 of 47 checks. Originals came back exactly, and real TTL expiry was followed by a clean recompression.

Capacity eviction behaved differently. With an in-memory store set to two entries, three compressed inputs push out the first original. Compress that first input again and Headroom returns the same cached reference, which still points at nothing. All three originals restored correctly before the repeat. The capacity suite passes 3 of 4 checks. A separately checked fallback to the original messages brings the combined report to 4 of 5, without changing the upstream behaviour.

The compressed text is lossy, so a dead reference means the original is gone unless you kept it. Check that the reference still resolves when you reuse a compressed result, and keep originals for later misses. That check can't prevent an eviction that happens after it runs.

## Reproduce

From the fixture bundle's root:

```sh
sh grinder/20261101-headroom/setup.sh
grinder/20261101-headroom/.venv/bin/python grinder/20261101-headroom/verify.py
```

Versions: headroom-ai 0.42.0, Python 3.13.9, with all 69 installed distributions pinned in `requirements.txt`. The fixture files are not published with this note yet.

## Not verified

These are synthetic local SDK calls on an explicit in-memory store. The default SQLite backend, shared stores, concurrency, proxy tool dispatch, model answer quality and production readiness were not tested. A related TTL issue on the OpenAI Responses adapter is [#4145](https://github.com/headroomlabs-ai/headroom/issues/4145); this one is capacity eviction on a different path. No upstream report has been filed for it.
