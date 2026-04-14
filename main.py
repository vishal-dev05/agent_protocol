"""
Autonomous AI Agent Protocol - FastAPI Backend
Author: [Your Name]
Description: A platform where AI agents can register, search, call each other, and track usage.
"""

from fastapi import FastAPI, HTTPException
from models import Agent, Usage
from storage import agents, usage_logs, request_ids

app = FastAPI(
    title="Autonomous AI Agent Protocol",
    description="A platform for registering, discovering, and tracking AI agents.",
    version="1.0.0"
)


# ──────────────────────────────────────────────
# PART 1: AGENT REGISTRY
# ──────────────────────────────────────────────

@app.post("/agents", summary="Register a new agent")
def add_agent(agent: Agent):
    """
    Register a new AI agent.
    - Rejects duplicate agent names (400 error).
    - Automatically extracts keyword tags from the description.
    """
    if agent.name in agents:
        raise HTTPException(status_code=400, detail=f"Agent '{agent.name}' already exists.")

    # BONUS: Extract tags from description for smarter search
    agent.tags = extract_tags(agent.description)
    agents[agent.name] = agent

    return {"message": f"Agent '{agent.name}' registered successfully.", "tags": agent.tags}


@app.get("/agents", summary="List all registered agents")
def list_agents():
    """Return all registered agents."""
    return agents


@app.get("/search", summary="Search agents by keyword")
def search_agents(q: str):
    """
    Search agents by name, description, or tags.
    Case-insensitive partial match supported.
    """
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")

    result = []
    q_lower = q.lower().strip()

    for agent in agents.values():
        # Match against name, description, or any tag
        if (
            q_lower in agent.name.lower()
            or q_lower in agent.description.lower()
            or any(q_lower in tag for tag in agent.tags)
        ):
            result.append(agent)

    return result


# ──────────────────────────────────────────────
# PART 2: USAGE LOGGING
# ──────────────────────────────────────────────

@app.post("/usage", summary="Log a usage event between agents")
def log_usage(usage: Usage):
    """
    Log when one agent calls another.

    Edge Cases Handled:
    1. Duplicate request_id → idempotent: ignored silently (prevents double billing).
    2. Unknown caller or target agent → 400 error.
    3. Missing fields → handled automatically by Pydantic validation.
    """

    # EDGE CASE 1: Idempotency — ignore duplicate request IDs
    if usage.request_id in request_ids:
        return {"message": "Duplicate request ignored (idempotent)."}

    # EDGE CASE 2: Validate both agents exist
    if usage.caller not in agents:
        raise HTTPException(status_code=400, detail=f"Unknown caller agent: '{usage.caller}'.")
    if usage.target not in agents:
        raise HTTPException(status_code=400, detail=f"Unknown target agent: '{usage.target}'.")

    # All checks passed — log the usage
    request_ids.add(usage.request_id)
    usage_logs.append(usage)

    return {"message": "Usage logged successfully."}


@app.get("/usage-summary", summary="Get usage summary per agent")
def usage_summary():
    """
    Returns total units consumed per agent (as the target/callee).
    Useful for billing and analytics.
    """
    summary = {}

    for log in usage_logs:
        summary[log.target] = summary.get(log.target, 0) + log.units

    return summary


@app.get("/usage-logs", summary="View raw usage logs")
def get_usage_logs():
    """Return all raw usage log entries."""
    return usage_logs


# ──────────────────────────────────────────────
# BONUS: NLP TAG EXTRACTION
# ──────────────────────────────────────────────

def extract_tags(description: str) -> list[str]:
    """
    Extract meaningful keyword tags from a description.
    Filters out common English stopwords for cleaner results.
    """
    stopwords = {
        "the", "is", "from", "and", "a", "an", "to", "of",
        "in", "for", "on", "with", "that", "this", "it", "at"
    }
    words = description.lower().split()
    tags = [w.strip(".,!?") for w in words if w not in stopwords and len(w) > 2]
    return list(set(tags))
