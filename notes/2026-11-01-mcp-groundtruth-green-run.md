---
title: "A green conformance run can contain a real violation"
date: 2026-11-01
tags: [mcp, testing, agents, provenance]
source: https://pypi.org/project/mcp-groundtruth/0.3.0/
---

# A green conformance run can contain a real violation

I tested MCP-groundtruth 0.3.0 on synthetic servers. The tool separates two jobs that are easy to confuse: checking its own known-answer fixtures, and auditing a server.

Seven published fixtures matched all 52 declared expectations, including tools built to lie about their hints. That result says the checker works on those fixtures. It says nothing about any other server.

Exit codes need the same care. A known violation returned exit 0 in ordinary audit mode, and adding `--fail-on-violation` returned 1. A CI job that runs the audit without that flag stays green while the report lists a violation.

A stricter gate over the reports closes that gap. It requires a reviewed inventory of properties, verified resets, complete declared observer coverage, stable controls and PASS for every requested property. It passed 32 of 32 checks using real reports and malformed-evidence mutations. Missing declarations, partial coverage and NOT_APPLICABLE stay unverified rather than counting as a pass. The gate does not authenticate reports, and it cannot find state the observer definition leaves out.

A separate six-check test found a provenance limit. Fixture code that Git ignores, sitting beneath a repository, gets the enclosing HEAD and `git_dirty=false`, even after that code changes. The content digest does change. Treat the digest and the package pin as the identity evidence, since the enclosing Git metadata does not pin the files that ran.

## Evidence

Versions: MCP-groundtruth 0.3.0, MCP Python SDK 2.3.0, CPython 3.13.9. The recorded results are public in [agent-claims](https://github.com/maxmorrish/agent-claims/tree/67d8a73/evidence/20261029-groundtruth). They are archived results: the runnable fixture is not published yet, so they can be read but not rerun.

## Not verified

Only synthetic fixture servers were tested. Live servers and the native network observer were not. No upstream report has been filed for the provenance behaviour.
