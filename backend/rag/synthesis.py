import os
from typing import Optional
import google.generativeai as genai
from .models import RagPrompt

class SynthesisService:
    """
    Client routing prompt payloads to configured Gemini LLM synthesis endpoints.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        
        # Fallback to reading from .env file directly if env var is empty
        if not self.api_key and os.path.exists(".env"):
            try:
                with open(".env", "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("GEMINI_API_KEY="):
                            self.api_key = line.split("=", 1)[1].strip()
                            break
            except Exception:
                pass
        
        if self.api_key:
            genai.configure(api_key=self.api_key)

    def synthesize(self, prompt: RagPrompt) -> str:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not configured. Provide it via constructor or environment variable.")
        
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=prompt.system_instruction
        )
        response = model.generate_content(prompt.user_prompt)
        return response.text
