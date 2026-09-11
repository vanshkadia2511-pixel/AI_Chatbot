"""
StudyBuddy - Modern 3-Panel AI Learning Application
Interactive nav, full-height chat, complete 5-page system.
"""

import streamlit as st
from config import (
    DEFAULT_MODEL, LEARNING_MODES, PREDEFINED_SUBJECTS,
    DIFFICULTY_LEVELS, get_api_key,
)
from prompts import get_system_instruction
from gemini_client import GeminiManager, GeminiClientError
import quiz_manager as qm

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StudyBuddy - AI Learning Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body { height: 100vh !important; overflow: hidden !important; font-family: 'Inter', sans-serif !important; }
[class*="css"] { font-family: 'Inter', sans-serif !important; }

/* ── Kill chrome ── */
header, #MainMenu, footer,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stAppDeployButton"], [data-testid="stStatusWidget"],
[data-testid="collapsedControl"] { display: none !important; }

/* ── Force full viewport height on entire Streamlit app ── */
.stApp { height: 100vh !important; overflow: hidden !important; }
.block-container { padding: 0 !important; max-width: 100vw !important; height: 100vh !important; overflow: hidden !important; }
[data-testid="stMainBlockContainer"] { padding: 0 !important; height: 100vh !important; overflow: hidden !important; }
section[data-testid="stMain"] { height: 100vh !important; overflow: hidden !important; }
section[data-testid="stMain"] > div:first-child { padding: 0 !important; height: 100% !important; }

/* ── Columns stretch to full height ── */
[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
    align-items: stretch !important;
    height: 100vh !important;
}
[data-testid="column"] { padding: 0 !important; height: 100vh !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
.stMarkdown { margin: 0 !important; }

/* ═══════════════ LEFT COLUMN ═══════════════ */
[data-testid="column"]:nth-child(1) {
    background: #ffffff !important;
    border-right: 1.5px solid #E8EDF5 !important;
    height: 100vh !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
}
[data-testid="column"]:nth-child(1)::-webkit-scrollbar { display: none; }

/* Logo block */
.sb-logo-block {
    display: flex; align-items: center; gap: 11px;
    padding: 20px 16px 16px 16px;
    border-bottom: 1px solid #EEEDF5;
    background: #fff;
}
.sb-logo-icon {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
    box-shadow: 0 4px 10px rgba(79,70,229,0.3);
}
.sb-logo-title { font-size: 17px; font-weight: 800; color: #1E293B; line-height: 1.2; }
.sb-logo-tag   { font-size: 10px; color: #94A3B8; font-weight: 500; letter-spacing: 0.02em; }

/* NAV BUTTONS — override Streamlit to look like sidebar nav */
[data-testid="column"]:nth-child(1) .stButton > button {
    width: 100% !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 10px 14px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    border-radius: 10px !important;
    border: none !important;
    background: transparent !important;
    color: #64748B !important;
    box-shadow: none !important;
    margin: 1px 0 !important;
    transition: all 0.18s ease !important;
}
[data-testid="column"]:nth-child(1) .stButton > button:hover {
    background: #F0F4FF !important;
    color: #4F46E5 !important;
}
/* Active nav item — set via data attribute trick via class on wrapper */
.nav-active .stButton > button {
    background: #4F46E5 !important;
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(79,70,229,0.3) !important;
}
.nav-active .stButton > button:hover {
    background: #4338CA !important;
    color: #fff !important;
}

/* SDG card in left panel */
.sb-sdg-card {
    margin: 12px 10px 8px 10px;
    padding: 14px;
    background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
    border-radius: 14px;
    border: 1px solid #BFDBFE;
}
.sb-sdg-row { display: flex; align-items: center; gap: 8px; margin-bottom: 7px; }
.sb-sdg-num {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #DC2626, #B91C1C);
    border-radius: 8px; display: flex;
    align-items: center; justify-content: center;
    font-size: 15px; font-weight: 800; color: #fff; flex-shrink: 0;
}
.sb-sdg-sup  { font-size: 10px; color: #1D4ED8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
.sb-sdg-t1   { font-size: 13px; font-weight: 700; color: #1E3A8A; margin-bottom: 2px; }
.sb-sdg-t2   { font-size: 11.5px; color: #3B82F6; line-height: 1.5; }

/* Mascot card */
.sb-mascot-card {
    margin: 0 10px 10px 10px;
    padding: 12px 14px;
    background: linear-gradient(135deg, #F5F3FF, #EDE9FE);
    border-radius: 14px; border: 1px solid #DDD6FE;
    display: flex; align-items: center; gap: 10px;
}
.sb-mascot-emoji { font-size: 32px; }
.sb-mascot-txt   { font-size: 11px; color: #6D28D9; font-weight: 600; line-height: 1.5; }

/* ═══════════════ CENTER COLUMN ═══════════════ */
[data-testid="column"]:nth-child(2) {
    background: #F8FAFF !important;
    height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
}
/* Make the inner vertical block a flex column too */
[data-testid="column"]:nth-child(2) > [data-testid="stVerticalBlock"] {
    height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
}
/* Chat messages area — scrollable, fills remaining space */
[data-testid="column"]:nth-child(2) [data-testid="stChatMessageContainer"] {
    flex: 1 !important;
    overflow-y: auto !important;
    padding: 12px 0 !important;
}
/* Chat input wrapper — always pinned to bottom */
[data-testid="column"]:nth-child(2) [data-testid="stBottom"] {
    position: sticky !important;
    bottom: 0 !important;
    background: #F8FAFF !important;
    padding: 10px 0 14px !important;
    border-top: 1px solid #E8EDF5 !important;
    z-index: 10 !important;
}

/* Hero banner */
.sb-hero {
    padding: 18px 28px 14px;
    background: #ffffff;
    border-bottom: 1px solid #E8EDF5;
    display: flex; align-items: center; justify-content: space-between;
    flex-shrink: 0;
}
.sb-hero h1 { font-size: 21px; font-weight: 800; color: #1E293B; margin-bottom: 3px; }
.sb-hero h1 span { color: #4F46E5; }
.sb-hero p  { font-size: 13px; color: #64748B; line-height: 1.5; max-width: 380px; }
.sb-hero-em { font-size: 52px; line-height: 1; }

/* API key warning */
.sb-api-warn {
    margin: 12px 28px 0;
    background: #FFF7ED; border: 1px solid #FED7AA;
    border-radius: 10px; padding: 10px 14px;
    font-size: 12.5px; color: #9A3412; font-weight: 500;
    flex-shrink: 0;
}

/* Welcome card (when no messages yet) */
.sb-welcome-card {
    background: #fff; border: 1px solid #E8EDF5;
    border-radius: 16px; padding: 28px 32px;
    text-align: center; max-width: 500px; width: 90%;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}
.sb-welcome-card .wc-ico { font-size: 46px; margin-bottom: 12px; }
.sb-welcome-card h3 { font-size: 17px; font-weight: 700; color: #1E293B; margin-bottom: 8px; }
.sb-welcome-card p  { font-size: 13px; color: #64748B; line-height: 1.7; }
.wc-meta {
    display: inline-block; margin-top: 12px;
    background: #EEF2FF; color: #4F46E5;
    border-radius: 8px; padding: 5px 14px;
    font-size: 12px; font-weight: 600;
}

/* Vertically centre the welcome card in remaining space */
.sb-center-fill {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    flex: 1; padding: 24px 20px;
    min-height: 0;   /* prevents flex child from overflowing */
}

/* Chat bubbles — override Streamlit defaults */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 4px 0 !important;
}
[data-testid="stChatInput"] {
    border: 2px solid #E2E8F0 !important;
    border-radius: 14px !important;
    background: #fff !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05) !important;
    font-size: 14px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #4F46E5 !important;
    box-shadow: 0 4px 20px rgba(79,70,229,0.12) !important;
}

/* ═══════════════ RIGHT COLUMN ═══════════════ */
[data-testid="column"]:nth-child(3) {
    background: #ffffff !important;
    border-left: 1.5px solid #E8EDF5 !important;
    height: 100vh !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
}
[data-testid="column"]:nth-child(3)::-webkit-scrollbar { width: 3px; }
[data-testid="column"]:nth-child(3)::-webkit-scrollbar-thumb { background: #E2E8F0; border-radius: 99px; }

/* Right panel section headings */
.r-head {
    font-size: 12px; font-weight: 700; color: #374151;
    margin: 0 0 8px 0;
    display: flex; align-items: center; gap: 5px;
}
hr.r-div { border: none; border-top: 1px solid #F1F5F9; margin: 12px 0; }

/* Right panel Streamlit widgets */
[data-testid="column"]:nth-child(3) div[data-testid="stSelectbox"] label,
[data-testid="column"]:nth-child(3) div[data-testid="stTextInput"] label {
    font-size: 12px !important; font-weight: 600 !important; color: #374151 !important;
}
[data-testid="column"]:nth-child(3) div[data-testid="stSelectbox"] > div > div {
    background: #F8FAFF !important; border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important; font-size: 13px !important;
}
[data-testid="column"]:nth-child(3) div[data-testid="stTextInput"] input {
    background: #F8FAFF !important; border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important; font-size: 13px !important;
}

/* Right panel buttons */
[data-testid="column"]:nth-child(3) .stButton > button {
    border-radius: 10px !important; font-size: 13px !important; font-weight: 600 !important;
    border: 1px solid #E2E8F0 !important; background: #F8FAFF !important;
    color: #374151 !important; transition: all 0.18s !important;
}
[data-testid="column"]:nth-child(3) .stButton > button:hover {
    background: #EEF2FF !important; border-color: #C7D2FE !important; color: #4F46E5 !important;
}
[data-testid="column"]:nth-child(3) .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
    color: white !important; border: none !important;
    box-shadow: 0 4px 12px rgba(79,70,229,0.3) !important;
}

/* SDG bottom note */
.sb-sdg-note {
    background: linear-gradient(135deg, #F0FDF4, #DCFCE7);
    border: 1px solid #BBF7D0; border-radius: 12px;
    padding: 12px; font-size: 11.5px; color: #166534;
    font-weight: 500; line-height: 1.6; text-align: center;
}

/* ─── Quiz ─── */
.quiz-q-box {
    background: #fff; border: 1px solid #E8EDF5;
    border-left: 5px solid #4F46E5; border-radius: 12px;
    padding: 18px 22px; font-size: 15px; font-weight: 600;
    color: #1E293B; margin-bottom: 14px; line-height: 1.5;
}
.score-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: #EEF2FF; color: #4F46E5;
    padding: 5px 14px; border-radius: 20px;
    font-size: 13px; font-weight: 700; border: 1px solid #C7D2FE;
}

/* ─── Study Resources cards ─── */
.res-card {
    background: #fff; border: 1px solid #E8EDF5;
    border-radius: 14px; padding: 16px 18px; margin-bottom: 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}
.res-card-title { font-size: 14px; font-weight: 700; color: #1E293B; margin-bottom: 3px; }
.res-card-desc  { font-size: 12.5px; color: #64748B; line-height: 1.5; }

/* ─── Progress stats ─── */
.prog-stat {
    background: #fff; border: 1px solid #E8EDF5;
    border-radius: 14px; padding: 16px 10px; text-align: center;
}
.prog-stat .val { font-size: 28px; font-weight: 800; color: #4F46E5; }
.prog-stat .lbl { font-size: 12px; color: #64748B; font-weight: 500; margin-top: 3px; }

/* ─── Settings ─── */
.settings-box {
    background: #fff; border: 1px solid #E8EDF5;
    border-radius: 14px; padding: 18px 20px; margin-bottom: 12px;
}
.settings-title { font-size: 14px; font-weight: 700; color: #1E293B; margin-bottom: 12px; }

/* ─── Topic row ─── */
.topic-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 7px 0; border-bottom: 1px solid #F1F5F9; font-size: 13px;
}
.topic-row:last-child { border-bottom: none; }
.topic-name { font-weight: 600; color: #374151; }
.topic-cnt  { font-size: 11px; color: #94A3B8; }

</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
for k, v in {
    "messages": [], "mode": "Study Mode",
    "subject": PREDEFINED_SUBJECTS[0], "custom_subject": "", "topic": "",
    "difficulty": DIFFICULTY_LEVELS[1], "user_api_key": "",
    "recent_topics": [], "active_nav": "Chat",
    "total_messages": 0, "total_quizzes": 0, "total_score": 0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

qm.initialize_quiz_session()

api_key        = get_api_key(st.session_state.user_api_key)
gemini_mgr     = GeminiManager(api_key=api_key)
effective_subj = (
    st.session_state.custom_subject
    if st.session_state.subject == "Other (Specify Below)" and st.session_state.custom_subject.strip()
    else st.session_state.subject
)

# ── Layout ────────────────────────────────────────────────────────────────────
left, center, right = st.columns([1.05, 3.85, 1.6], gap="small")

# ╔══════════════════════════════════════════════════════╗
# ║  LEFT PANEL                                          ║
# ╚══════════════════════════════════════════════════════╝
with left:
    # Logo
    st.markdown("""
    <div class="sb-logo-block">
        <div class="sb-logo-icon">🎓</div>
        <div>
            <div class="sb-logo-title">StudyBuddy</div>
            <div class="sb-logo-tag">Learn · Practice · Grow</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Nav items — each wrapped in active/inactive class
    nav_items = [
        ("💬", "Chat"),
        ("🧩", "Quiz Mode"),
        ("📚", "Study Resources"),
        ("📊", "Progress"),
        ("⚙️", "Settings"),
    ]
    for icon, label in nav_items:
        is_active = st.session_state.active_nav == label
        st.markdown(f'<div class="{"nav-active" if is_active else "nav-inactive"}" style="padding:0 8px;">', unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state.active_nav = label
            if label == "Chat":
                st.session_state.mode = "Study Mode"
            elif label == "Quiz Mode":
                st.session_state.mode = "Quiz Mode"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # SDG badge
    st.markdown("""
    <div class="sb-sdg-card">
        <div class="sb-sdg-row">
            <div class="sb-sdg-num">4</div>
            <span class="sb-sdg-sup">Supporting</span>
        </div>
        <div class="sb-sdg-t1">SDG 4 – Quality Education</div>
        <div class="sb-sdg-t2">Better learning today, a brighter tomorrow.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # Mascot
    st.markdown("""
    <div class="sb-mascot-card">
        <span class="sb-mascot-emoji">🤖</span>
        <span class="sb-mascot-txt">Your AI<br>Learning<br>Companion!</span>
    </div>
    """, unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════╗
# ║  CENTER PANEL                                        ║
# ╚══════════════════════════════════════════════════════╝
with center:
    nav = st.session_state.active_nav

    # Hero header — changes per page
    heroes = {
        "Chat":            ("✨ Hello! I'm <span>StudyBuddy</span> ✨", "Your AI learning tutor — ask me anything!", "🎓"),
        "Quiz Mode":       ("🧩 Interactive <span>Quiz Mode</span>",    "AI-generated MCQs — test yourself one question at a time!", "📋"),
        "Study Resources": ("📚 <span>Study Resources</span>",          "Curated subjects and tips to help you master any topic.", "📖"),
        "Progress":        ("📊 Your <span>Progress</span>",            "Track quiz scores, sessions, and your learning journey.", "🏆"),
        "Settings":        ("⚙️ <span>Settings</span>",                 "Personalise your StudyBuddy experience.", "🛠️"),
    }
    h_title, h_sub, h_em = heroes.get(nav, ("StudyBuddy", "", "🎓"))

    st.markdown(f"""
    <div class="sb-hero">
        <div>
            <h1>{h_title}</h1>
            <p>{h_sub}</p>
        </div>
        <div class="sb-hero-em">{h_em}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── CHAT ──────────────────────────────────────────────────────────────────
    if nav == "Chat":
        if not gemini_mgr.is_configured():
            st.markdown('<div class="sb-api-warn">🔑 <strong>API Key Missing</strong> — paste your Gemini API key in the right panel to start chatting. <a href="https://aistudio.google.com/" target="_blank" style="color:#9A3412;">Get a free key →</a></div>', unsafe_allow_html=True)

        mode = st.session_state.mode
        welcome_map = {
            "Study Mode":  ("📚", "Welcome to Study Mode!", "Ask any question — I'll explain it step-by-step with examples and understanding checks."),
            "Exam Mode":   ("📝", "Exam Preparation Mode",  "Focused on high-yield content: definitions, formulas, common mistakes & model answers."),
            "Explain Mode":("💡", "Progressive Explain Mode","Every concept explained at 3 levels: Simple → College Standard → Advanced Insight."),
        }

        if not st.session_state.messages:
            ico, title, desc = welcome_map.get(mode, ("🎓", "Welcome!", ""))
            st.markdown(f"""
            <div class="sb-center-fill">
                <div class="sb-welcome-card">
                    <div class="wc-ico">{ico}</div>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                    <span class="wc-meta">{effective_subj} &nbsp;|&nbsp; {st.session_state.topic or 'All Topics'}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="🧑‍🎓" if msg["role"] == "user" else "🤖"):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Type your message here..."):
            if not gemini_mgr.is_configured():
                st.error("🔑 Enter your Gemini API Key in the right panel first.")
            else:
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.total_messages += 1
                tk = st.session_state.topic or effective_subj
                found = [t for t in st.session_state.recent_topics if t["name"] == tk]
                if found:
                    found[0]["count"] += 1
                else:
                    st.session_state.recent_topics.insert(0, {"name": tk, "count": 1})
                    st.session_state.recent_topics = st.session_state.recent_topics[:5]

                with st.chat_message("user", avatar="🧑‍🎓"):
                    st.markdown(prompt)
                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner("Thinking..."):
                        try:
                            resp = gemini_mgr.generate_chat_response(
                                messages=st.session_state.messages,
                                system_instruction=get_system_instruction(
                                    mode=st.session_state.mode,
                                    subject=effective_subj,
                                    topic=st.session_state.topic,
                                    difficulty=st.session_state.difficulty,
                                ),
                                model_name=DEFAULT_MODEL,
                            )
                            st.markdown(resp)
                            st.session_state.messages.append({"role": "assistant", "content": resp})
                        except GeminiClientError as e:
                            st.error(str(e))
                        except Exception as e:
                            st.error(f"Unexpected error: {e}")

    # ── QUIZ MODE ─────────────────────────────────────────────────────────────
    elif nav == "Quiz Mode":
        st.markdown("<div style='padding:16px 28px;'>", unsafe_allow_html=True)
        qs = st.session_state.quiz_state

        if not gemini_mgr.is_configured():
            st.warning("🔑 Enter your Gemini API Key in the right panel to generate questions.")

        if not qs["active"] or qs["subject"] != effective_subj:
            st.markdown(f"""
            <div class="sb-center-fill">
                <div class="sb-welcome-card" style="max-width:480px;">
                    <div class="wc-ico">🧩</div>
                    <h3>Ready for a Quiz?</h3>
                    <p>AI-generated multiple-choice questions on <strong>{effective_subj}</strong>,
                    one at a time with instant feedback and scoring.</p>
                    <span class="wc-meta">Topic: {st.session_state.topic or 'All Topics'} &nbsp;|&nbsp; Level: {st.session_state.difficulty.split(' ')[0]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1.5, 1.2, 1.5])
            with c2:
                if st.button("🚀 Start Quiz", type="primary", use_container_width=True, disabled=not gemini_mgr.is_configured()):
                    qm.start_new_quiz(effective_subj, st.session_state.topic, st.session_state.difficulty)
                    st.session_state.total_quizzes += 1
                    with st.spinner("Generating your first question..."):
                        qm.fetch_next_question(gemini_mgr)
                    st.rerun()
        else:
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"<h4 style='margin:0;color:#1E293B;'>Question #{qs['question_number']}</h4>", unsafe_allow_html=True)
            with c2:
                answered = max(1, qs["question_number"] - (0 if qs["answered"] else 1))
                st.markdown(f"<div class='score-badge'>🏆 {qs['score']} / {answered}</div>", unsafe_allow_html=True)
            st.progress(min(1.0, qs["question_number"] / 10.0))
            st.write("")

            if qs["error_msg"]:
                st.error(qs["error_msg"])
                if st.button("🔄 Retry"):
                    with st.spinner("Retrying..."): qm.fetch_next_question(gemini_mgr)
                    st.rerun()
            elif qs["current_question"]:
                q = qs["current_question"]
                st.markdown(f"<div class='quiz-q-box'>❓ {q['question']}</div>", unsafe_allow_html=True)
                opts = q.get("options", {})
                correct = q.get("correct_option", "").strip().upper()

                if not qs["answered"]:
                    sel = st.radio("Choose your answer:", options=list(opts.keys()),
                                   format_func=lambda o: f"{o}:  {opts[o]}", index=None,
                                   key=f"qr_{qs['question_number']}")
                    ca, cb = st.columns([1, 3])
                    with ca:
                        if st.button("✅ Submit", type="primary", use_container_width=True, disabled=sel is None):
                            if sel:
                                qm.submit_answer(sel)
                                st.rerun()
                    with cb:
                        if q.get("hint"):
                            with st.expander("💡 Hint"):
                                st.info(q["hint"])
                else:
                    ua = qs["user_answer"]
                    if ua == correct:
                        st.success(f"🎉 **Correct!** → **{ua}:** {opts.get(ua, '')}")
                    else:
                        st.error(f"❌ You chose **{ua}** | Correct: **{correct}:** {opts.get(correct, '')}")
                    with st.expander("📖 Explanation", expanded=True):
                        st.info(q.get("explanation", ""))
                    ca, cb = st.columns(2)
                    with ca:
                        if st.button("➡️ Next Question", type="primary", use_container_width=True):
                            with st.spinner("Loading..."): qm.fetch_next_question(gemini_mgr)
                            st.rerun()
                    with cb:
                        if st.button("🏁 End Quiz", use_container_width=True):
                            st.info(f"**Quiz Complete!** Score: **{qs['score']} / {qs['question_number']}** 🎓")
                            qm.start_new_quiz(effective_subj, st.session_state.topic, st.session_state.difficulty)
                            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── STUDY RESOURCES ───────────────────────────────────────────────────────
    elif nav == "Study Resources":
        st.markdown("<div style='padding:16px 28px;'>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#EEF2FF;border-radius:12px;padding:12px 16px;margin-bottom:18px;font-size:13px;color:#4F46E5;font-weight:600;">
            💡 <strong>Tip:</strong> Click <strong>Study</strong> next to any subject to load it and start chatting!
        </div>
        """, unsafe_allow_html=True)

        resources = [
            ("📐", "Mathematics & Statistics",  "Algebra, Calculus, Probability, Statistics, Linear Algebra"),
            ("⚛️", "Physics",                    "Mechanics, Thermodynamics, Electromagnetism, Quantum Physics"),
            ("🧪", "Chemistry",                  "Organic, Inorganic, Physical Chemistry, Electrochemistry"),
            ("💻", "Computer Science & Programming", "Data Structures, Algorithms, OS, DBMS, Networks, OOP"),
            ("⚡", "Electronics & Electrical",   "Circuit Theory, Digital Electronics, Microprocessors"),
            ("📈", "Business & Economics",        "Microeconomics, Macroeconomics, Finance, Marketing"),
            ("🧬", "Biology",                    "Cell Biology, Genetics, Ecology, Biochemistry"),
            ("📜", "History & Social Sciences",  "World History, Political Science, Sociology, Geography"),
        ]
        for icon, name, desc in resources:
            c1, c2 = st.columns([4.5, 1])
            with c1:
                st.markdown(f"""
                <div class="res-card">
                    <div class="res-card-title">{icon} {name}</div>
                    <div class="res-card-desc">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                if st.button("📖 Study", key=f"res_{name}", use_container_width=True):
                    if name in PREDEFINED_SUBJECTS:
                        st.session_state.subject = name
                    else:
                        st.session_state.subject = "Other (Specify Below)"
                        st.session_state.custom_subject = name
                    st.session_state.mode = "Study Mode"
                    st.session_state.active_nav = "Chat"
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── PROGRESS ──────────────────────────────────────────────────────────────
    elif nav == "Progress":
        st.markdown("<div style='padding:16px 28px;'>", unsafe_allow_html=True)
        hist  = st.session_state.quiz_state.get("history", [])
        acc   = f"{round(st.session_state.total_score / max(1, len(hist)) * 100)}%" if hist else "N/A"
        c1, c2, c3, c4 = st.columns(4)
        for col, val, lbl in [
            (c1, st.session_state.total_messages, "Messages Sent"),
            (c2, st.session_state.total_quizzes,  "Quizzes Started"),
            (c3, st.session_state.total_score,    "Correct Answers"),
            (c4, acc,                             "Quiz Accuracy"),
        ]:
            with col:
                st.markdown(f'<div class="prog-stat"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)
        st.write("")
        st.markdown("### 📖 Quiz History")
        if not hist:
            st.info("No quiz history yet. Head to **Quiz Mode** to get started!")
        else:
            for h in reversed(hist[-10:]):
                ri = "✅" if h["is_correct"] else "❌"
                st.markdown(f"""
                <div class="res-card">
                    <div class="res-card-title">{ri} Q{h['question_num']}: {h['question'][:80]}{'...' if len(h['question'])>80 else ''}</div>
                    <div class="res-card-desc">Your answer: <strong>{h['user_answer']}</strong> | Correct: <strong>{h['correct_answer']}</strong></div>
                </div>
                """, unsafe_allow_html=True)
        st.write("")
        st.markdown("### 💬 Recent Topics Studied")
        if not st.session_state.recent_topics:
            st.info("No topics studied yet. Start chatting to track progress!")
        else:
            for t in st.session_state.recent_topics:
                st.markdown(f"""
                <div class="topic-row">
                    <div><div class="topic-name">{t['name']}</div><div class="topic-cnt">{t['count']} message(s)</div></div>
                    <div style="color:#CBD5E1;">›</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── SETTINGS ──────────────────────────────────────────────────────────────
    elif nav == "Settings":
        st.markdown("<div style='padding:16px 28px;'>", unsafe_allow_html=True)

        # API Key
        st.markdown('<div class="settings-box"><div class="settings-title">🔑 Gemini API Key</div>', unsafe_allow_html=True)
        if api_key:
            st.success("✅ API Key is configured and active.")
            if st.button("🔄 Replace API Key"):
                st.session_state.user_api_key = ""
                st.rerun()
        else:
            nk = st.text_input("Enter your Gemini API Key", type="password", placeholder="AQ....")
            if nk:
                st.session_state.user_api_key = nk
                st.rerun()
            st.caption("[Get your free key at Google AI Studio →](https://aistudio.google.com/)")
        st.markdown('</div>', unsafe_allow_html=True)

        # Preferences
        st.markdown('<div class="settings-box"><div class="settings-title">🎨 Learning Preferences</div>', unsafe_allow_html=True)
        pm = st.selectbox("Default Learning Mode", list(LEARNING_MODES.keys()),
                          index=list(LEARNING_MODES.keys()).index(st.session_state.mode))
        pd = st.selectbox("Default Difficulty Level", DIFFICULTY_LEVELS,
                          index=DIFFICULTY_LEVELS.index(st.session_state.difficulty))
        if st.button("💾 Save Preferences", type="primary"):
            st.session_state.mode = pm
            st.session_state.difficulty = pd
            st.success("✅ Preferences saved!")
        st.markdown('</div>', unsafe_allow_html=True)

        # Data management
        st.markdown('<div class="settings-box"><div class="settings-title">🗑️ Data Management</div>', unsafe_allow_html=True)
        ca, cb = st.columns(2)
        with ca:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.total_messages = 0
                st.toast("Chat cleared!", icon="🧹")
                st.rerun()
        with cb:
            if st.button("♻️ Reset All", use_container_width=True):
                for k in ["messages", "recent_topics"]:
                    st.session_state[k] = [] if isinstance(st.session_state[k], list) else {}
                for k in ["total_messages", "total_quizzes", "total_score"]:
                    st.session_state[k] = 0
                qm.initialize_quiz_session()
                st.toast("All data reset!", icon="♻️")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # About
        st.markdown('<div class="settings-box"><div class="settings-title">ℹ️ About StudyBuddy</div>', unsafe_allow_html=True)
        st.markdown("""
        **StudyBuddy** v1.0.0 — AI-powered learning companion for college students.
        Built with Python + Streamlit + Google Gemini API.

        - **SDG Alignment**: Goal 4 — Quality Education 🌱
        - **Model**: Google Gemini Flash
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════╗
# ║  RIGHT PANEL                                         ║
# ╚══════════════════════════════════════════════════════╝
with right:
    st.markdown("<div style='padding:18px 14px 20px;'>", unsafe_allow_html=True)

    # API key prompt (only when not configured)
    if not gemini_mgr.is_configured():
        st.markdown('<div class="r-head">🔑 API Key</div>', unsafe_allow_html=True)
        kv = st.text_input("key", type="password", placeholder="Paste Gemini API key...", label_visibility="collapsed")
        if kv:
            st.session_state.user_api_key = kv
            st.rerun()
        st.markdown('<hr class="r-div"/>', unsafe_allow_html=True)

    # Learning Mode
    st.markdown('<div class="r-head">⚡ Learning Mode</div>', unsafe_allow_html=True)
    mk = list(LEARNING_MODES.keys())
    sm = st.selectbox("Mode", mk, index=mk.index(st.session_state.mode),
                      format_func=lambda m: f"{LEARNING_MODES[m]['icon']} {m}",
                      label_visibility="collapsed")
    if sm != st.session_state.mode:
        st.session_state.mode = sm
        st.session_state.active_nav = "Quiz Mode" if sm == "Quiz Mode" else "Chat"
        st.rerun()
    st.caption(LEARNING_MODES[sm]["description"])
    st.markdown('<hr class="r-div"/>', unsafe_allow_html=True)

    # Subject / Topic
    st.markdown('<div class="r-head">📖 Subject / Topic</div>', unsafe_allow_html=True)
    ss = st.selectbox("Subj", PREDEFINED_SUBJECTS,
                      index=PREDEFINED_SUBJECTS.index(st.session_state.subject) if st.session_state.subject in PREDEFINED_SUBJECTS else 0,
                      label_visibility="collapsed")
    st.session_state.subject = ss
    if ss == "Other (Specify Below)":
        st.session_state.custom_subject = st.text_input("Custom subject", value=st.session_state.custom_subject,
                                                         placeholder="e.g. Quantum Computing...", label_visibility="collapsed")
    st.session_state.topic = st.text_input("Topic (optional)", value=st.session_state.topic,
                                            placeholder="e.g. Neural Networks...", label_visibility="collapsed")
    st.caption("Narrows the AI's focus to a specific topic")
    st.markdown('<hr class="r-div"/>', unsafe_allow_html=True)

    # Learner Level
    st.markdown('<div class="r-head">📊 Learner Level</div>', unsafe_allow_html=True)
    sd = st.selectbox("Diff", DIFFICULTY_LEVELS,
                      index=DIFFICULTY_LEVELS.index(st.session_state.difficulty) if st.session_state.difficulty in DIFFICULTY_LEVELS else 1,
                      format_func=lambda d: d.split(" ")[0],
                      label_visibility="collapsed")
    st.session_state.difficulty = sd
    st.caption("Adjusts explanation depth to your level")
    st.markdown('<hr class="r-div"/>', unsafe_allow_html=True)

    # Quick Actions
    st.markdown('<div class="r-head">⚡ Quick Actions</div>', unsafe_allow_html=True)
    if st.button("🧩 Start a Quiz", use_container_width=True):
        st.session_state.mode = "Quiz Mode"
        st.session_state.active_nav = "Quiz Mode"
        qm.start_new_quiz(effective_subj, st.session_state.topic, st.session_state.difficulty)
        st.session_state.total_quizzes += 1
        with st.spinner("Generating first question..."):
            qm.fetch_next_question(gemini_mgr)
        st.rerun()
    if st.button("💡 Explain Mode", use_container_width=True):
        st.session_state.mode = "Explain Mode"
        st.session_state.active_nav = "Chat"
        st.rerun()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.toast("Chat cleared!", icon="🧹")
        st.rerun()
    st.markdown('<hr class="r-div"/>', unsafe_allow_html=True)

    # Recent Topics
    if st.session_state.recent_topics:
        st.markdown('<div class="r-head">🕒 Recent Topics</div>', unsafe_allow_html=True)
        for t in st.session_state.recent_topics[:4]:
            st.markdown(f"""
            <div class="topic-row">
                <div><div class="topic-name">{t['name']}</div><div class="topic-cnt">{t['count']} message(s)</div></div>
                <div style="color:#CBD5E1;font-size:14px;">›</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('<hr class="r-div"/>', unsafe_allow_html=True)

    # SDG note
    st.markdown('<div class="sb-sdg-note">🌱 Together we can make quality education accessible to everyone! 🌍</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
