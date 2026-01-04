"""Interview API endpoints."""
import logging
from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import (
    CreateInterviewRequest,
    CreateInterviewResponse,
    InterviewResponseRequest,
    InterviewerResponse,
    InterviewStateResponse,
    InterviewMeta
)
from app.core.state_manager import (
    create_interview_state,
    get_interview_state,
    update_interview_state
)
from app.agents.interviewer_agent import interviewer_agent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.post("", response_model=CreateInterviewResponse, status_code=status.HTTP_201_CREATED)
async def create_interview(request: CreateInterviewRequest):
    """
    Create a new interview session.
    
    Returns interview ID and initial interviewer question.
    """
    try:
        # Generate candidate ID
        candidate_id = uuid4()
        
        # Create interview state
        state = create_interview_state(
            candidate_id=candidate_id,
            candidate_name=request.candidate_name,
            theory_topic=request.theory_topic,
            interview_type=request.interview_type,
            coding_problem_id=request.coding_problem_id
        )
        
        # Get initial question from interviewer
        response = await interviewer_agent.get_initial_question(state)
        
        # Add interviewer message to transcript
        state.add_message("assistant", response["speech"])
        
        # Update state
        update_interview_state(state)
        
        return CreateInterviewResponse(
            interview_id=state.interview_id,
            candidate_id=candidate_id,
            message="Interview created successfully",
            interviewer_response=InterviewerResponse(
                speech=response["speech"],
                meta=InterviewMeta(**response["meta"])
            )
        )
        
    except Exception as e:
        logger.error(f"Error creating interview: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create interview: {str(e)}"
        )


@router.get("/{interview_id}", response_model=InterviewStateResponse)
async def get_interview(interview_id: UUID):
    """Get interview state."""
    state = get_interview_state(interview_id)
    
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    return InterviewStateResponse(
        interview_id=state.interview_id,
        candidate_id=state.candidate_id,
        candidate_name=state.candidate_name,
        current_phase=state.current_phase,
        theory_phase=state.theory_phase,
        theory_topic=state.theory_topic,
        theory_followups_asked=state.theory_followups_asked,
        created_at=state.created_at,
        updated_at=state.updated_at
    )


@router.post("/{interview_id}/respond", response_model=InterviewerResponse)
async def submit_response(interview_id: UUID, request: InterviewResponseRequest):
    """
    Submit a candidate response and get interviewer's next question.
    
    This is the main interaction endpoint for Phase 1 (text-only).
    """
    # Get interview state
    state = get_interview_state(interview_id)
    
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    if state.current_phase == "complete":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview is already complete"
        )
    
    try:
        # Add user message to transcript
        state.add_message("user", request.message)
        
        # Get interviewer response
        response = await interviewer_agent.respond(state, user_message=request.message)
        
        # Add interviewer response to transcript
        if response["speech"]:
            state.add_message("assistant", response["speech"])
        
        # Update state
        update_interview_state(state)
        
        return InterviewerResponse(
            speech=response["speech"],
            meta=InterviewMeta(**response["meta"])
        )
        
    except Exception as e:
        logger.error(f"Error processing response: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process response: {str(e)}"
        )

