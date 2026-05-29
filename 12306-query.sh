#!/bin/bash
# Wrapper: restart 12306-mcp before each query to avoid "Already connected" bug
pkill -f "12306-mcp" 2>/dev/null
sleep 0.5
12306-mcp --host localhost --port 8080 > /tmp/12306-mcp.log 2>&1 &
sleep 2
cd /root/concert-trip-planner-skill/.agents/skills/12306-smart-query
/root/.venv-12306/bin/python scripts/train_query.py "$@"
