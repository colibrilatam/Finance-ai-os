#!/usr/bin/env bash
set -euo pipefail
for u in http://localhost:8088/health http://localhost:8088/api/customer http://localhost:8088/api/metrics; do echo "== $u"; curl -fsS "$u"; echo; done
echo "MCP endpoint: http://localhost:8090/mcp"
