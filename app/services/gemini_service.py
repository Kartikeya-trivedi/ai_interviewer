"""Gemini API service with retry and circuit breaker."""
import json
import logging
import asyncio
from typing import Dict, Any, Optional
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from app.config import settings

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini API."""
    
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        # Create models with system instructions (will be set per-request)
        self.interviewer_model_name = settings.gemini_model_interviewer
        self.judge_model_name = settings.gemini_model_judge
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def generate_response(
        self,
        prompt: str,
        system_instruction: str,
        model_type: str = "interviewer",
        temperature: float = 0.7,
        max_output_tokens: int = 500
    ) -> str:
        """
        Generate a response from Gemini.
        
        Args:
            prompt: User prompt
            system_instruction: System instruction
            model_type: "interviewer" or "judge"
            temperature: Sampling temperature
            max_output_tokens: Maximum output tokens
        
        Returns:
            Generated text response
        """
        try:
            model_name = self.interviewer_model_name if model_type == "interviewer" else self.judge_model_name
            
            # Create model with system instruction
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
            
            # Configure safety settings (permissive for interview context)
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            
            # Configure generation parameters
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
            }
            
            # Run synchronous Gemini API call in thread pool
            response = await asyncio.to_thread(
                model.generate_content,
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}", exc_info=True)
            raise
    
    async def generate_json_response(
        self,
        prompt: str,
        system_instruction: str,
        model_type: str = "interviewer"
    ) -> Dict[str, Any]:
        """
        Generate a JSON response from Gemini.
        
        Args:
            prompt: User prompt
            system_instruction: System instruction
            model_type: "interviewer" or "judge"
        
        Returns:
            Parsed JSON response
        """
        # Request JSON format
        json_prompt = f"{prompt}\n\nIMPORTANT: Respond with valid JSON only. No markdown, no code blocks."
        
        response_text = await self.generate_response(
            json_prompt,
            system_instruction,
            model_type=model_type,
            temperature=0.3  # Lower temperature for structured output
        )
        
        # Clean response (remove markdown code blocks if present)
        cleaned = response_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {cleaned[:200]}")
            raise ValueError(f"Invalid JSON response from Gemini: {e}")


# Global instance
gemini_service = GeminiService()

