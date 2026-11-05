---
title: "Three findings from 3,269 small claims about agent tooling"
date: 2026-11-05
tags: [agents, testing, evals]
source: https://github.com/maxmorrish/agent-claims
---

# Three findings from 3,269 small claims about agent tooling

Between October and early November I tested 3,269 narrow claims across 140 dated test folders, mostly about agent libraries, MCP servers and model clients. 2,123 have clean reruns, 65 need host setup to rerun, and 1,081 are archive-only. No outcome changed on rerun. The corpus is now archived read-only; these are the three results that held up best.

**Complete JSON can come from incomplete gzip.** Ordinary HTTPX2 decoding met 12 of 33 input-integrity expectations. A bounded decoder met 33 of 33.

**A passing upstream suite can miss fidelity failures.** The same skills-ref source passed 40 of 40 of its own tests but met 6 of 12 added XML path-fidelity expectations. The two denominators describe different test sets, so neither number contradicts the other.

**Harness exit zero is not success.** 278 cleanly reproduced failing claims came from harness runs that exited zero and recorded their failures in structured results. Anything that reads only the exit code would have counted them as passes.

The third finding is the one I'm following up: a CI check that catches runs reporting success when their own results say otherwise.

## Reproduce

```sh
git clone https://github.com/maxmorrish/agent-claims && cd agent-claims
python3 -m unittest discover -s tests -v
python3 scripts/rerun.py --all --output results/local.jsonl
```

## Not verified

The archive-only rows were not rerun. Counts are from the corpus as of 2026-11-03.
