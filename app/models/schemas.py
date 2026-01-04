"""Pydantic schemas for API requests and responses."""
from datetime import datetime
from typing import Optional, List, Literal
from uuid import UUID
from pydantic import BaseModel, Field


# Request Schemas
class CreateInterviewRequest(BaseModel):
    """Request to create a new interview."""
    candidate_name: str = Field(..., min_length=1, max_length=100)
    interview_type: str = "ml_junior"
    theory_topic: str = Field(..., min_length=1)
    coding_problem_id: Optional[str] = None


class InterviewResponseRequest(BaseModel):
    """Request to submit a candidate response."""
    message: str = Field(..., min_length=1, max_length=2000)


# Response Schemas
class InterviewMeta(BaseModel):
    """Interview metadata in response."""
    phase: int
    followup_used: bool
    flag_vague: bool
    flag_incorrect: bool
    end_theory_round: bool


class InterviewerResponse(BaseModel):
    """Interviewer agent response."""
    speech: str
    meta: InterviewMeta


class InterviewStateResponse(BaseModel):
    """Interview state response."""
    interview_id: UUID
    candidate_id: UUID
    candidate_name: str
    current_phase: Literal["theory", "coding", "complete"]
    theory_phase: int
    theory_topic: str
    theory_followups_asked: int
    created_at: datetime
    updated_at: datetime


class CreateInterviewResponse(BaseModel):
    """Response after creating an interview."""
    interview_id: UUID
    candidate_id: UUID
    message: str
    interviewer_response: InterviewerResponse


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

