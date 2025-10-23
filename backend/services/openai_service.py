import os
from openai import OpenAI
from typing import List, Dict
from ..schemas.conversation import AIResponse

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=api_key)
        self.available_models = [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-turbo",
            "gpt-4o",
        ]

    async def get_response(self, messages: List[Dict[str, str]], model: str = "gpt-4") -> AIResponse:
        """Get AI response from OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            return AIResponse(
                content=response.choices[0].message.content.strip(),
                model=model
            )
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return self.available_models

# Global instance
openai_service = OpenAIService()