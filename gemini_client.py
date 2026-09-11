"""
Gemini API Integration Module
Handles client creation, message history conversion, model generation, and error handling.
"""

from typing import List, Dict, Any, Optional, Generator
import os
from google import genai
from google.genai import types

from config import DEFAULT_MODEL, FALLBACK_MODEL, get_api_key

class GeminiClientError(Exception):
    """Custom exception for user-friendly error reporting."""
    pass

class GeminiManager:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = get_api_key(api_key)
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                raise GeminiClientError(f"Failed to initialize Gemini Client: {str(e)}")

    def is_configured(self) -> bool:
        """Returns True if the API key is present and client initialized."""
        return self.client is not None

    def _convert_messages_to_sdk_contents(
        self, messages: List[Dict[str, str]]
    ) -> List[types.Content]:
        """
        Converts list of standard message dicts [{"role": "user"/"assistant", "content": "..."}]
        into google-genai SDK types.Content objects.
        """
        sdk_contents = []
        for msg in messages:
            role = msg.get("role", "user")
            content_text = msg.get("content", "")
            
            # Map assistant role to SDK model role
            sdk_role = "model" if role in ["assistant", "model"] else "user"
            
            if content_text and content_text.strip():
                sdk_contents.append(
                    types.Content(
                        role=sdk_role,
                        parts=[types.Part.from_text(text=content_text)]
                    )
                )
        return sdk_contents

    def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_instruction: str,
        temperature: float = 0.7,
        model_name: str = DEFAULT_MODEL,
    ) -> str:
        """
        Generates a chat completion given message history and system instruction.
        Handles model fallbacks and API errors gracefully.
        """
        if not self.is_configured():
            raise GeminiClientError(
                "Gemini API key is not configured. Please enter your API key in the sidebar or set GEMINI_API_KEY in your .env file."
            )

        sdk_contents = self._convert_messages_to_sdk_contents(messages)
        if not sdk_contents:
            raise GeminiClientError("No content provided to send to Gemini.")

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
        )

        try:
            # Try primary model
            response = self.client.models.generate_content(
                model=model_name,
                contents=sdk_contents,
                config=config,
            )
            return response.text if response.text else "I apologize, but I could not generate a response for that prompt."

        except Exception as primary_err:
            err_msg = str(primary_err).lower()
            
            # Catch specific errors
            if "api_key" in err_msg or "unauthorized" in err_msg or "403" in err_msg or "401" in err_msg:
                raise GeminiClientError(
                    "🔑 Invalid API Key. Please verify your Gemini API key from Google AI Studio (https://aistudio.google.com/)."
                )
            elif "quota" in err_msg or "429" in err_msg or "resource_exhausted" in err_msg:
                raise GeminiClientError(
                    "⏳ Gemini API rate limit or quota exceeded. Please wait a moment before trying again."
                )

            # Try fallback model if model_name was DEFAULT_MODEL
            if model_name != FALLBACK_MODEL:
                try:
                    response = self.client.models.generate_content(
                        model=FALLBACK_MODEL,
                        contents=sdk_contents,
                        config=config,
                    )
                    return response.text if response.text else "No response text generated."
                except Exception as fallback_err:
                    raise GeminiClientError(f"Error communicating with Gemini API: {str(fallback_err)}")
            
            raise GeminiClientError(f"Error communicating with Gemini API: {str(primary_err)}")

    def generate_single_response(
        self,
        prompt: str,
        system_instruction: str,
        temperature: float = 0.5,
        model_name: str = DEFAULT_MODEL,
    ) -> str:
        """
        Single-turn generation helper for Quiz generation or quick tasks.
        """
        messages = [{"role": "user", "content": prompt}]
        return self.generate_chat_response(
            messages=messages,
            system_instruction=system_instruction,
            temperature=temperature,
            model_name=model_name,
        )
