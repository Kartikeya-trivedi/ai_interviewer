"""Interviewer agent - voice-facing, theory interview."""
import logging
from typing import Dict, Any, Optional
from app.core.state_manager import InterviewState
from app.core.prompts import INTERVIEWER_THEORY_PROMPT
from app.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)


class InterviewerAgent:
    """Interviewer agent for theory interviews."""
    
    def __init__(self):
        self.gemini = gemini_service
    
    async def respond(
        self,
        state: InterviewState,
        user_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate interviewer response based on current state.
        
        Args:
            state: Current interview state
            user_message: Optional user message (for follow-ups)
        
        Returns:
            Response dict with "speech" and "meta" keys
        """
        try:
            # Build context prompt
            context = self._build_context(state, user_message)
            
            # Get system instruction
            system_instruction = INTERVIEWER_THEORY_PROMPT.format(
                theory_topic=state.theory_topic
            )
            
            # Generate response
            response = await self.gemini.generate_json_response(
                prompt=context,
                system_instruction=system_instruction,
                model_type="interviewer"
            )
            
            # Validate response structure
            if "speech" not in response or "meta" not in response:
                raise ValueError("Invalid response structure from Gemini")
            
            # Update state based on meta
            self._update_state_from_meta(state, response["meta"])
            
            return response
            
        except Exception as e:
            logger.error(f"Interviewer agent error: {e}", exc_info=True)
            # Fallback response
            return {
                "speech": "I apologize, could you repeat that?",
                "meta": {
                    "phase": state.theory_phase,
                    "followup_used": False,
                    "flag_vague": False,
                    "flag_incorrect": False,
                    "end_theory_round": False
                }
            }
    
    def _build_context(self, state: InterviewState, user_message: Optional[str]) -> str:
        """Build context prompt for Gemini."""
        context_parts = [
            f"Interview State:",
            f"- Current Phase: {state.current_phase}",
            f"- Theory Phase: {state.theory_phase}",
            f"- Theory Topic: {state.theory_topic}",
            f"- Follow-ups Asked: {state.theory_followups_asked}",
            f"- Candidate: {state.candidate_name}",
            "",
            "Recent Transcript:"
        ]
        
        # Add last 5 messages for context
        recent_messages = state.transcript[-5:] if len(state.transcript) > 5 else state.transcript
        for msg in recent_messages:
            context_parts.append(f"{msg.role}: {msg.content}")
        
        if user_message:
            context_parts.append(f"\nLatest User Message: {user_message}")
        
        context_parts.append(
            "\nGenerate your next response following the rules. "
            "If this is the first message, ask the Phase 1 core concept question."
        )
        
        return "\n".join(context_parts)
    
    def _update_state_from_meta(self, state: InterviewState, meta: Dict[str, Any]):
        """Update state based on agent meta response."""
        # Update flags
        if meta.get("flag_vague"):
            state.set_flag("vague", True)
        if meta.get("flag_incorrect"):
            state.set_flag("incorrect", True)
        
        # Track follow-ups
        if meta.get("followup_used"):
            state.theory_followups_asked += 1
        
        # Advance phase if needed
        if meta.get("end_theory_round"):
            state.current_phase = "coding"
        elif state.theory_phase < 3 and state.theory_followups_asked >= 2:
            state.advance_phase()
    
    async def get_initial_question(self, state: InterviewState) -> Dict[str, Any]:
        """Get the initial question for the interview."""
        return await self.respond(state, user_message=None)


# Global instance
interviewer_agent = InterviewerAgent()

