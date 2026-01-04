"""Interview state management - external state, not LLM-managed."""
from datetime import datetime
from typing import List, Dict, Literal, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Transcript message."""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CodeResult(BaseModel):
    """Code execution result."""
    submission_id: UUID
    language: str
    code: str
    compiled: bool
    tests_passed: int = 0
    tests_failed: int = 0
    runtime_ms: Optional[float] = None
    error: Optional[str] = None
    submitted_at: datetime = Field(default_factory=datetime.utcnow)


class InterviewState(BaseModel):
    """Interview state schema - critical for flow control."""
    interview_id: UUID
    candidate_id: UUID
    candidate_name: str
    
    # Flow control
    current_phase: Literal["theory", "coding", "complete"] = "theory"
    theory_phase: int = 1  # 1, 2, 3
    theory_followups_asked: int = 0  # max 2
    coding_mode: Literal["problem", "silent", "discussion", "end"] = "problem"
    
    # Content tracking
    theory_topic: str
    coding_problem_id: Optional[str] = None
    transcript: List[Message] = Field(default_factory=list)
    
    # Flags (for judge)
    flags: Dict[str, bool] = Field(default_factory=dict)  # vague, incorrect, hand_waving, cargo_cult
    
    # Compiler results
    code_submissions: List[CodeResult] = Field(default_factory=list)
    
    # Timestamps
    phase_start_times: Dict[str, datetime] = Field(default_factory=dict)
    silence_duration: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Metadata
    language: str = "python"
    difficulty: str = "junior"
    interview_type: str = "ml_junior"
    
    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
    
    def add_message(self, role: Literal["user", "assistant"], content: str):
        """Add a message to the transcript."""
        self.transcript.append(Message(role=role, content=content))
        self.update_timestamp()
    
    def set_flag(self, flag_name: str, value: bool = True):
        """Set a flag for the judge."""
        self.flags[flag_name] = value
        self.update_timestamp()
    
    def advance_phase(self):
        """Advance to the next theory phase."""
        if self.current_phase == "theory":
            if self.theory_phase < 3:
                self.theory_phase += 1
            else:
                self.current_phase = "coding"
        self.update_timestamp()
    
    def add_code_submission(self, result: CodeResult):
        """Add a code submission result."""
        self.code_submissions.append(result)
        self.update_timestamp()


# In-memory state store (Phase 1 - will move to DB in Phase 4)
_state_store: Dict[UUID, InterviewState] = {}


def create_interview_state(
    candidate_id: UUID,
    candidate_name: str,
    theory_topic: str,
    interview_type: str = "ml_junior",
    coding_problem_id: Optional[str] = None
) -> InterviewState:
    """Create a new interview state."""
    interview_id = uuid4()
    state = InterviewState(
        interview_id=interview_id,
        candidate_id=candidate_id,
        candidate_name=candidate_name,
        theory_topic=theory_topic,
        interview_type=interview_type,
        coding_problem_id=coding_problem_id,
        phase_start_times={"theory": datetime.utcnow()}
    )
    _state_store[interview_id] = state
    return state


def get_interview_state(interview_id: UUID) -> Optional[InterviewState]:
    """Get interview state by ID."""
    return _state_store.get(interview_id)


def update_interview_state(state: InterviewState) -> InterviewState:
    """Update interview state in store."""
    state.update_timestamp()
    _state_store[state.interview_id] = state
    return state

