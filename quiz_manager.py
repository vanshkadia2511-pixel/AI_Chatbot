"""
Quiz Manager Module
Handles interactive multiple-choice question generation, answer evaluation,
score tracking, and quiz state management for Streamlit.
"""

import json
import re
from typing import Dict, Any, Optional
import streamlit as st

from gemini_client import GeminiManager, GeminiClientError
from prompts import get_quiz_generation_prompt, get_system_instruction

def initialize_quiz_session():
    """Initializes session state structure for Quiz Mode."""
    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = {
            "active": False,
            "subject": "",
            "topic": "",
            "difficulty": "",
            "current_question": None,
            "question_number": 0,
            "score": 0,
            "user_answer": None,
            "answered": False,
            "history": [],
            "error_msg": None,
        }

def start_new_quiz(subject: str, topic: str, difficulty: str):
    """Resets and initializes a fresh quiz session."""
    st.session_state.quiz_state = {
        "active": True,
        "subject": subject,
        "topic": topic,
        "difficulty": difficulty,
        "current_question": None,
        "question_number": 0,
        "score": 0,
        "user_answer": None,
        "answered": False,
        "history": [],
        "error_msg": None,
    }

def clean_json_response(raw_text: str) -> Dict[str, Any]:
    """Extracts and parses JSON object from LLM response string."""
    # Find JSON block inside ```json ... ``` or raw string
    json_match = re.search(r"```(?:json)?\s*({[\s\S]*?})\s*```", raw_text)
    if json_match:
        raw_json = json_match.group(1)
    else:
        # Fallback to finding first '{' and last '}'
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start != -1 and end != -1:
            raw_json = raw_text[start : end + 1]
        else:
            raw_json = raw_text

    try:
        return json.loads(raw_json)
    except Exception as e:
        raise ValueError(f"Failed to parse quiz question JSON: {str(e)}\nRaw response: {raw_text[:200]}")

def fetch_next_question(gemini_manager: GeminiManager) -> Optional[Dict[str, Any]]:
    """Generates the next quiz question using Gemini API."""
    state = st.session_state.quiz_state
    
    prompt = get_quiz_generation_prompt(
        subject=state["subject"],
        topic=state["topic"],
        difficulty=state["difficulty"],
    )
    system_inst = get_system_instruction(
        mode="Quiz Mode",
        subject=state["subject"],
        topic=state["topic"],
        difficulty=state["difficulty"],
    )

    try:
        raw_response = gemini_manager.generate_single_response(
            prompt=prompt,
            system_instruction=system_inst,
            temperature=0.4,
        )
        q_data = clean_json_response(raw_response)
        
        # Validate expected keys
        required_keys = ["question", "options", "correct_option", "explanation"]
        for key in required_keys:
            if key not in q_data:
                raise ValueError(f"Missing required key '{key}' in quiz output.")
        
        state["current_question"] = q_data
        state["question_number"] += 1
        state["user_answer"] = None
        state["answered"] = False
        state["error_msg"] = None
        return q_data
    except Exception as err:
        state["error_msg"] = f"Unable to generate quiz question: {str(err)}"
        return None

def submit_answer(selected_option: str):
    """Processes the student's selected answer and updates score."""
    state = st.session_state.quiz_state
    if not state["current_question"] or state["answered"]:
        return

    state["user_answer"] = selected_option
    state["answered"] = True
    correct_option = state["current_question"].get("correct_option", "").strip().upper()
    
    is_correct = selected_option.upper() == correct_option
    if is_correct:
        state["score"] += 1

    state["history"].append({
        "question_num": state["question_number"],
        "question": state["current_question"]["question"],
        "options": state["current_question"]["options"],
        "user_answer": selected_option,
        "correct_answer": correct_option,
        "is_correct": is_correct,
        "explanation": state["current_question"]["explanation"],
    })
