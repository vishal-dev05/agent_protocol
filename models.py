"""
Data models for the Autonomous AI Agent Protocol.
Uses Pydantic for automatic validation and clear error messages.
"""

from pydantic import BaseModel, Field
from typing import List


class Agent(BaseModel):
    """Represents an AI agent registered on the platform."""
    name: str = Field(..., min_length=1, description="Unique name of the agent")
    description: str = Field(..., min_length=5, description="What this agent does")
    endpoint: str = Field(..., description="URL or identifier where this agent can be called")
    tags: List[str] = Field(default=[], description="Auto-extracted keyword tags")


class Usage(BaseModel):
    """Represents a single usage event — one agent calling another."""
    caller: str = Field(..., description="Name of the agent making the call")
    target: str = Field(..., description="Name of the agent being called")
    units: int = Field(..., gt=0, description="Units of compute/tokens consumed (must be > 0)")
    request_id: str = Field(..., min_length=1, description="Unique ID for idempotency")
