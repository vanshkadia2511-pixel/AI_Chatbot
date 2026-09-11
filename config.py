"""
StudyBuddy Configuration Module
Centralizes model selection, subject presets, difficulty levels, and secrets lookup.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Automatically load environment variables from local .env file
load_dotenv()

# Gemini Model Constants
DEFAULT_MODEL = "gemini-3.6-flash"
FALLBACK_MODEL = "gemini-flash-latest"

# Available Learning Modes
LEARNING_MODES = {
    "Study Mode": {
        "icon": "📚",
        "description": "Interactive study companion with clear explanations, real-world examples, and understanding checks.",
    },
    "Quiz Mode": {
        "icon": "🧩",
        "description": "Interactive 1-by-1 multiple-choice questions with immediate feedback and score tracking.",
    },
    "Exam Mode": {
        "icon": "📝",
        "description": "Exam-oriented revision focusing on core definitions, formulas, common pitfalls, and past paper style questions.",
    },
    "Explain Mode": {
        "icon": "💡",
        "description": "Progressive 3-level breakdown: Simple Analogy -> College Concept -> Deep Dive.",
    },
}

# Predefined Academic Subjects
PREDEFINED_SUBJECTS = [
    "Computer Science & Programming",
    "Mathematics & Statistics",
    "Physics",
    "Chemistry",
    "Electrical & Electronics Engineering",
    "Mechanical & Civil Engineering",
    "Business, Finance & Economics",
    "Biology & Biotechnology",
    "General Studies & Humanities",
    "Other (Specify Below)",
]

# Difficulty Levels
DIFFICULTY_LEVELS = [
    "Beginner (Foundational concepts)",
    "Intermediate (Standard college curriculum)",
    "Advanced (Deep analytical / theoretical)",
    "Exam-Focused (High-yield practice & formulas)",
]

def get_api_key(user_provided_key: Optional[str] = None) -> Optional[str]:
    """
    Retrieves the Gemini API Key checking multiple sources in priority order:
    1. Direct user input from Streamlit UI sidebar
    2. Local environment variable (GEMINI_API_KEY from .env)
    3. Fallback check for .env.example
    4. Streamlit Cloud Secrets (st.secrets["GEMINI_API_KEY"])
    """
    if user_provided_key and user_provided_key.strip():
        return user_provided_key.strip()
    
    # 2. Check environment variables (.env)
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key and env_key.strip() and not env_key.startswith("your_"):
        return env_key.strip()

    # 3. Check if .env.example has a valid key
    try:
        env_example_path = os.path.join(os.path.dirname(__file__), ".env.example")
        if os.path.exists(env_example_path):
            with open(env_example_path, "r") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        val = line.split("=", 1)[1].strip()
                        if val and not val.startswith("your_"):
                            return val
    except Exception:
        pass
    
    # 4. Check Streamlit secrets if available
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            secrets_key = st.secrets["GEMINI_API_KEY"]
            if secrets_key and str(secrets_key).strip():
                return str(secrets_key).strip()
    except Exception:
        pass
        
    return None

