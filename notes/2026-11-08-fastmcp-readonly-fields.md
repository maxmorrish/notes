---
title: "Hiding an API field does not stop it being sent"
date: 2026-11-08
tags: [mcp, fastmcp, openapi, testing]
source: https://github.com/PrefectHQ/fastmcp
---

# Hiding an API field does not stop it being sent

FastMCP 4.2.0a3 removes `readOnly` fields from the tool input schemas it generates from an OpenAPI spec, including nested and referenced fields. I tested whether that also stops a caller from sending them.

The test runs real in-memory client calls and captures the HTTP request bodies with a mock transport. It covers two OpenAPI dialects, three schema shapes, and strict validation on and off. FastMCP 4.2.0a3 meets 114 of 126 expectations; 4.1.6 meets 66 of 126. All 48 schema differences between the versions are improvements. The remaining 12 failures come from six strict-mode calls that still send a `readOnly` field when the caller supplies one.

The upstream change keeps the parameter mapping on purpose, so this is a boundary rather than a bug. The field disappears from what the model is shown. Nothing stops it reaching your API if a caller includes it anyway, so the backend still has to reject it.

## Evidence

Versions: FastMCP 4.2.0a3 and 4.1.6. The runnable fixture is not published yet, so the numbers can be read here but not rerun.

## Not verified

Backend enforcement, authentication, a live transport, whole-body array parameters, and `prefixItems` in OpenAPI 3.1.
