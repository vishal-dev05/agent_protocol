"""
In-memory storage for the Autonomous AI Agent Protocol.

In production, this would be replaced with:
- agents       → PostgreSQL table with indexed name/description
- usage_logs   → Append-only PostgreSQL or time-series DB
- request_ids  → Redis SET for fast O(1) deduplication at scale
"""

agents = {}          # key: agent name → value: Agent object
usage_logs = []      # list of all Usage log entries
request_ids = set()  # set of seen request_ids (for idempotency)
