"""
StudyBuddy External API
Lightweight FastAPI REST endpoint implementing POST /chat.
Uses the same StudyBuddy core (system prompt, Gemini integration) as the Streamlit web UI.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

from config import DEFAULT_MODEL, get_api_key
from prompts import get_system_instruction
from gemini_client import GeminiManager, GeminiClientError

# ---------------------------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="StudyBuddy API",
    description="AI Learning Tutor REST API — SDG 4: Quality Education",
    version="1.0.0",
)

# CORS — allow evaluation systems and external tools to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    """Incoming chat request body."""
    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The user's learning question or message.",
        examples=["Teach me the basics of linear regression."],
    )
    subject: Optional[str] = Field(
        default="General",
        description="Academic subject area (e.g. Mathematics, Physics, Computer Science).",
    )
    level: Optional[str] = Field(
        default="Intermediate (Standard college curriculum)",
        description="Learner difficulty level.",
    )
    mode: Optional[str] = Field(
        default="Study Mode",
        description="Learning mode: Study Mode, Explain Mode, Exam Mode.",
    )


class ChatResponse(BaseModel):
    """Successful chat response."""
    response: str


class ErrorResponse(BaseModel):
    """Error response."""
    error: str


# ---------------------------------------------------------------------------
# Gemini Manager (singleton for the API process)
# ---------------------------------------------------------------------------
_gemini_manager: Optional[GeminiManager] = None


def _get_gemini_manager() -> GeminiManager:
    """Lazy-initialise and return the Gemini manager."""
    global _gemini_manager
    if _gemini_manager is None or not _gemini_manager.is_configured():
        api_key = get_api_key()
        if not api_key:
            raise HTTPException(
                status_code=503,
                detail={"error": "Server API key is not configured. Set GEMINI_API_KEY in environment."},
            )
        _gemini_manager = GeminiManager(api_key=api_key)
    return _gemini_manager


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "ok",
        "service": "StudyBuddy API",
        "version": "1.0.0",
        "sdg": "SDG 4 — Quality Education",
    }


# ---------------------------------------------------------------------------
# POST /chat — Main Competition Endpoint
# ---------------------------------------------------------------------------
@app.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "AI generation failure"},
        503: {"model": ErrorResponse, "description": "Service unavailable"},
    },
    tags=["Chat"],
    summary="Send a learning question and receive a StudyBuddy response",
)
async def chat(request: ChatRequest):
    """
    Main chat endpoint. Accepts a user message and returns the StudyBuddy AI response.

    Uses the same core logic (system prompt, Gemini integration, mode modifiers)
    as the Streamlit web UI — no separate implementation.

    **Contract (matches competition specification):**

    Request:
    ```json
    { "message": "Teach me the basics of linear regression." }
    ```

    Response:
    ```json
    { "response": "..." }
    ```
    """
    # Validate message content
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail={"error": "Invalid request. The 'message' field must not be empty."},
        )

    try:
        manager = _get_gemini_manager()

        # Build system instruction — identical to what the Streamlit UI uses
        system_instruction = get_system_instruction(
            mode=request.mode or "Study Mode",
            subject=request.subject or "General",
            topic="",
            difficulty=request.level or "Intermediate (Standard college curriculum)",
        )

        # Call the same StudyBuddy core
        messages = [{"role": "user", "content": request.message.strip()}]
        response_text = manager.generate_chat_response(
            messages=messages,
            system_instruction=system_instruction,
            model_name=DEFAULT_MODEL,
        )

        return ChatResponse(response=response_text)

    except GeminiClientError as e:
        # Known API errors (auth, rate limit, etc.) — return 500 with friendly message
        raise HTTPException(
            status_code=500,
            detail={"error": "Unable to generate a response right now."},
        )
    except HTTPException:
        # Re-raise HTTP exceptions (e.g. 503 from missing key)
        raise
    except Exception:
        # Unexpected errors — never expose internals
        raise HTTPException(
            status_code=500,
            detail={"error": "Unable to generate a response right now."},
        )


# ---------------------------------------------------------------------------
# Run with: uvicorn api:app --host 0.0.0.0 --port 8000
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
