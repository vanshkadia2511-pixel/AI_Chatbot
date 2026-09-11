"""
StudyBuddy — Ultra Master Frontend Implementation
Built according to complete product specifications for SDG 4 Quality Education.
"""
import datetime
import streamlit as st
from config import (
    DEFAULT_MODEL, LEARNING_MODES, PREDEFINED_SUBJECTS,
    DIFFICULTY_LEVELS, get_api_key,
)
from prompts import get_system_instruction
from gemini_client import GeminiManager
import quiz_manager as qm

# Page setup
st.set_page_config(
    page_title="StudyBuddy – AI Learning Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

_hour = datetime.datetime.now().hour
_greeting = "Good Morning" if _hour < 12 else ("Good Afternoon" if _hour < 17 else "Good Evening")

# Initialize Session State
for k, v in {
    "messages": [],
    "mode": "Study Mode",
    "subject": PREDEFINED_SUBJECTS[0],
    "custom_subject": "",
    "topic": "",
    "difficulty": DIFFICULTY_LEVELS[1],
    "user_api_key": "",
    "recent_topics": [],
    "active_nav": "Chat",
    "total_messages": 0,
    "total_quizzes": 0,
    "total_score": 0,
    "theme": "light",
    "profile": "Student 🧑‍🎓",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

qm.initialize_quiz_session()
api_key = get_api_key(st.session_state.user_api_key)
gemini_mgr = GeminiManager(api_key=api_key)
eff_subj = (
    st.session_state.custom_subject
    if st.session_state.subject == "Other (Specify Below)" and st.session_state.custom_subject.strip()
    else st.session_state.subject
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS DESIGN SYSTEM & DYNAMIC TOKENS
# ══════════════════════════════════════════════════════════════════════════════
is_dark = st.session_state.theme == "dark"

bg_page = "#0F172A" if is_dark else "#FFFFFF"
bg_side = "#1E293B" if is_dark else "#FAFAFA"
bg_card = "#1E293B" if is_dark else "#FFFFFF"
border_col = "#334155" if is_dark else "#F0F0F0"
border_card = "#334155" if is_dark else "#EFEFEF"
text_main = "#F8FAFC" if is_dark else "#111827"
text_sub = "#94A3B8" if is_dark else "#6B7280"
text_muted = "#64748B" if is_dark else "#9CA3AF"
active_bg = "#312E81" if is_dark else "#EEF2FF"
active_txt = "#818CF8" if is_dark else "#4F46E5"
chip_bg = "#1E293B" if is_dark else "#F5F5F5"
user_msg_bg = "#1E293B" if is_dark else "#EEF2FF"
user_msg_border = "#334155" if is_dark else "#C7D2FE"

st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*,*::before,*::after{{box-sizing:border-box;}}
html,body{{height:100vh;overflow:hidden;margin:0;padding:0;}}
body,[class*="css"]{{font-family:'Inter',sans-serif!important;background:{bg_page}!important;color:{text_main}!important;}}
header,#MainMenu,footer,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stAppDeployButton"],[data-testid="stStatusWidget"],
[data-testid="collapsedControl"]{{display:none!important;}}
.stApp{{height:100vh!important;overflow:hidden!important;background:{bg_page}!important;}}
.block-container{{padding:0!important;max-width:100vw!important;height:100vh!important;overflow:hidden!important;}}
[data-testid="stMainBlockContainer"]{{padding:0!important;height:100vh!important;overflow:hidden!important;}}
section[data-testid="stMain"]{{height:100vh!important;overflow:hidden!important;background:{bg_page}!important;}}
section[data-testid="stMain"]>div:first-child{{padding:0!important;height:100%!important;}}
[data-testid="stHorizontalBlock"]{{gap:0!important;align-items:stretch!important;height:100vh!important;}}
[data-testid="column"]{{padding:0!important;height:100vh!important;}}
[data-testid="stVerticalBlock"]{{gap:0!important;}}
.stMarkdown{{margin:0!important;}}

/* ── LEFT SIDEBAR ── */
[data-testid="column"]:nth-child(1){{background:{bg_side}!important;border-right:1px solid {border_col}!important;height:100vh!important;overflow-y:auto!important;overflow-x:hidden!important;position:relative!important;display:flex!important;flex-direction:column!important;}}
.sb-logo{{display:flex;align-items:center;justify-content:space-between;padding:18px 16px 8px;}}
.sb-logo-left{{display:flex;align-items:center;gap:8px;}}
.sb-logo-icon{{font-size:22px;}}
.sb-logo-text{{font-size:16.5px;font-weight:800;color:{text_main};letter-spacing:-0.02em;}}
.sb-tagline{{font-size:10px;font-weight:600;color:{text_sub};letter-spacing:.05em;padding:0 16px 12px;text-transform:uppercase;}}
.sb-search-box{{margin:0 12px 10px;display:flex;align-items:center;gap:8px;background:{chip_bg};border:1px solid {border_card};border-radius:9px;padding:7px 11px;}}
.sb-search-box span{{font-size:12px;color:{text_muted};}}
.sb-search-box input{{border:none;background:transparent;outline:none;font-size:12px;color:{text_sub};width:100%;}}
.sb-kbd{{font-size:9.5px;color:{text_muted};background:{border_col};border-radius:4px;padding:1px 5px;font-weight:600;}}
.sb-nav-wrap{{padding:4px 8px 6px;}}
[data-testid="column"]:nth-child(1) .stButton>button{{width:100%!important;text-align:left!important;justify-content:flex-start!important;padding:8px 10px!important;font-size:13px!important;font-weight:500!important;border-radius:8px!important;border:none!important;background:transparent!important;color:{text_sub}!important;box-shadow:none!important;margin:1px 0!important;transition:all .15s!important;}}
[data-testid="column"]:nth-child(1) .stButton>button:hover{{background:{chip_bg}!important;color:{text_main}!important;}}
.nav-active .stButton>button{{background:{active_bg}!important;color:{active_txt}!important;font-weight:700!important;}}

/* SDG 4 Module Card */
.sb-sdg-card{{margin:8px 12px;background:linear-gradient(135deg,#0284C7,#0369A1);border-radius:12px;padding:12px 14px;color:#fff;box-shadow:0 4px 12px rgba(2,132,199,.2);}}
.sb-sdg-header{{display:flex;align-items:center;gap:8px;font-size:10px;font-weight:800;letter-spacing:.08em;background:rgba(255,255,255,.2);padding:2px 7px;border-radius:4px;width:fit-content;margin-bottom:6px;}}
.sb-sdg-title{{font-size:12px;font-weight:700;line-height:1.3;margin-bottom:4px;}}
.sb-sdg-msg{{font-size:10.5px;opacity:.9;font-style:italic;line-height:1.3;}}

/* Companion Mascot Card */
.sb-companion-card{{margin:6px 12px 12px;background:{bg_card};border:1px solid {border_card};border-radius:12px;padding:10px 12px;display:flex;align-items:center;gap:10px;}}
.sb-companion-avatar{{font-size:24px;width:36px;height:36px;background:linear-gradient(135deg,#818CF8,#C084FC);border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}}
.sb-companion-name{{font-size:11px;font-weight:700;color:{text_main};}}
.sb-companion-msg{{font-size:10px;font-weight:600;color:#6366F1;background:{active_bg};padding:2px 6px;border-radius:6px;width:fit-content;margin-top:2px;}}

.sb-hist-label{{font-size:10.5px;font-weight:700;color:{text_muted};padding:8px 16px 4px;letter-spacing:.04em;text-transform:uppercase;}}
.sb-hist-item{{padding:6px 14px;font-size:12px;color:{text_sub};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;border-radius:6px;margin:1px 6px;cursor:pointer;}}
.sb-hist-item:hover{{background:{chip_bg};color:{text_main};}}

.sb-user-card{{margin-top:auto;background:{bg_card};border-top:1px solid {border_col};padding:12px 14px;display:flex;align-items:center;justify-content:space-between;}}
.sb-user-left{{display:flex;align-items:center;gap:9px;}}
.sb-avatar{{width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#6366F1,#8B5CF6);display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;color:#fff;}}
.sb-u-name{{font-size:12px;font-weight:700;color:{text_main};}}
.sb-u-sub{{font-size:10px;color:{text_sub};}}

/* ── CENTER ── */
[data-testid="column"]:nth-child(2){{background:{bg_page}!important;height:100vh!important;display:flex!important;flex-direction:column!important;overflow:hidden!important;}}
[data-testid="column"]:nth-child(2)>[data-testid="stVerticalBlock"]{{height:100vh!important;display:flex!important;flex-direction:column!important;overflow:hidden!important;}}
.sb-topbar{{display:flex;align-items:center;justify-content:space-between;padding:10px 20px;border-bottom:1px solid {border_col};background:{bg_card};flex-shrink:0;}}
.sb-model-pill{{display:inline-flex;align-items:center;gap:7px;background:{chip_bg};border-radius:20px;padding:5px 13px;font-size:12.5px;font-weight:600;color:{text_main};border:1px solid {border_card};}}
.sb-model-dot{{width:18px;height:18px;border-radius:50%;background:linear-gradient(135deg,#818CF8,#C084FC);display:inline-flex;align-items:center;justify-content:center;font-size:9px;color:#fff;}}

[data-testid="column"]:nth-child(2) [data-testid="stHorizontalBlock"] .stButton>button{{border-radius:20px!important;font-size:12px!important;font-weight:700!important;padding:6px 13px!important;border:none!important;background:#111827!important;color:#fff!important;box-shadow:none!important;transition:background .15s!important;}}
[data-testid="column"]:nth-child(2) [data-testid="stHorizontalBlock"] .stButton>button:hover{{background:#374151!important;}}

/* Hero */
.sb-hero{{display:flex;flex-direction:column;align-items:center;justify-content:center;flex:1;padding:0 30px 20px;text-align:center;position:relative;overflow:hidden;}}
.sb-orb{{width:72px;height:72px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#A5B4FC,#818CF8 40%,#7C3AED 70%,#C084FC);margin-bottom:18px;box-shadow:0 0 45px rgba(129,140,248,.35);animation:orbpulse 3s ease-in-out infinite;}}
@keyframes orbpulse{{0%,100%{{box-shadow:0 0 45px rgba(129,140,248,.35);}}50%{{box-shadow:0 0 65px rgba(129,140,248,.55);}}}}
.sb-greet{{font-size:26px;font-weight:800;color:{text_main};line-height:1.3;margin-bottom:4px;}}
.sb-greet-sub{{font-size:26px;font-weight:800;background:linear-gradient(135deg,#6366F1,#A78BFA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.3;margin-bottom:20px;}}
.sb-subtitle{{font-size:13.5px;color:{text_sub};max-width:540px;line-height:1.6;margin-bottom:24px;}}
.sb-pastel-wash{{position:absolute;bottom:0;left:0;right:0;height:160px;background:linear-gradient(to top,rgba(99,102,241,.06) 0%,transparent 100%);pointer-events:none;}}

/* Chat area */
[data-testid="stChatMessageContainer"]{{flex:1!important;overflow-y:auto!important;padding:12px 24px!important;}}
[data-testid="stChatMessageContainer"]::-webkit-scrollbar{{width:4px;}}
[data-testid="stChatMessageContainer"]::-webkit-scrollbar-thumb{{background:{border_col};border-radius:99px;}}
[data-testid="stChatMessage"]{{background:transparent!important;padding:8px 12px!important;margin-bottom:8px!important;}}

/* Action Bar Pill Controls below assistant response */
.action-bar{{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-top:10px;padding-top:8px;border-top:1px dashed {border_card};}}

/* Chip-bar mode buttons */
.chip-row [data-testid="stHorizontalBlock"]{{height:auto!important;}}
.chip-row .stButton>button{{border-radius:20px!important;font-size:11.5px!important;font-weight:600!important;border:1px solid {border_card}!important;background:{chip_bg}!important;color:{text_sub}!important;padding:4px 11px!important;box-shadow:none!important;margin:0!important;transition:all .15s!important;}}
.chip-row .stButton>button:hover{{background:{active_bg}!important;border-color:{active_txt}!important;color:{active_txt}!important;}}
.chip-active .stButton>button{{background:{active_bg}!important;border-color:{active_txt}!important;color:{active_txt}!important;font-weight:700!important;}}

/* Chat input */
[data-testid="stBottom"]{{flex-shrink:0!important;padding:0!important;background:{bg_card}!important;border-top:1px solid {border_col}!important;}}
[data-testid="stChatInputTextArea"]{{font-size:13.5px!important;background:{bg_page}!important;color:{text_main}!important;}}

/* RIGHT PANEL */
[data-testid="column"]:nth-child(3){{background:{bg_side}!important;border-left:1px solid {border_col}!important;height:100vh!important;overflow-y:auto!important;overflow-x:hidden!important;}}
[data-testid="column"]:nth-child(3)::-webkit-scrollbar{{width:3px;}}
[data-testid="column"]:nth-child(3)::-webkit-scrollbar-thumb{{background:{border_col};border-radius:99px;}}
[data-testid="column"]:nth-child(3) .stButton>button{{border-radius:9px!important;font-size:12px!important;font-weight:600!important;border:1px solid {border_card}!important;background:{bg_card}!important;color:{text_main}!important;transition:all .15s!important;padding:7px 11px!important;box-shadow:none!important;}}
[data-testid="column"]:nth-child(3) .stButton>button:hover{{background:{active_bg}!important;border-color:{active_txt}!important;color:{active_txt}!important;}}
[data-testid="column"]:nth-child(3) .stButton>button[kind="primary"]{{background:linear-gradient(135deg,#6366F1,#8B5CF6)!important;color:#fff!important;border:none!important;box-shadow:0 4px 12px rgba(99,102,241,.3)!important;}}
[data-testid="column"]:nth-child(3) div[data-testid="stSelectbox"]>div>div{{background:{bg_card}!important;border:1px solid {border_card}!important;border-radius:9px!important;font-size:12.5px!important;color:{text_main}!important;}}
[data-testid="column"]:nth-child(3) div[data-testid="stTextInput"] input{{background:{bg_card}!important;border:1px solid {border_card}!important;border-radius:9px!important;font-size:12.5px!important;color:{text_main}!important;}}
[data-testid="column"]:nth-child(3) div[data-testid="stSelectbox"] label,[data-testid="column"]:nth-child(3) div[data-testid="stTextInput"] label{{font-size:10.5px!important;font-weight:700!important;color:{text_muted}!important;text-transform:uppercase!important;letter-spacing:.05em!important;}}
.r-card{{background:{bg_card};border:1px solid {border_card};border-radius:12px;padding:12px 14px;margin-bottom:10px;}}
.r-card-title{{font-size:10.5px;font-weight:700;color:{text_muted};text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px;}}

/* Adaptive Loop Indicator */
.adaptive-loop-box{{background:linear-gradient(135deg,rgba(99,102,241,.08),rgba(168,85,247,.08));border:1px solid rgba(99,102,241,.2);border-radius:10px;padding:10px 12px;margin-bottom:10px;}}
.adaptive-loop-title{{font-size:11px;font-weight:700;color:#6366F1;display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;}}
.adaptive-flow{{display:flex;align-items:center;gap:4px;font-size:10px;font-weight:600;color:{text_sub};}}
.adaptive-step{{background:{bg_card};border:1px solid {border_card};padding:2px 6px;border-radius:4px;}}
.adaptive-arrow{{color:#818CF8;font-size:10px;}}

.tp-row{{display:flex;align-items:center;justify-content:space-between;padding:6px 0;border-bottom:1px solid {border_card};}}
.tp-row:last-child{{border:none;}}
.tp-name{{font-size:12px;font-weight:600;color:{text_main};}}
.tp-cnt{{font-size:10.5px;color:{text_muted};}}

.quiz-q-box{{background:{bg_card};border:1px solid {border_card};border-left:4px solid #6366F1;border-radius:12px;padding:16px 20px;font-size:14px;font-weight:600;color:{text_main};margin-bottom:14px;line-height:1.5;}}
.q-score{{display:inline-flex;align-items:center;gap:5px;background:{active_bg};color:{active_txt};padding:4px 12px;border-radius:20px;font-size:12px;font-weight:700;border:1px solid {active_txt};}}
.res-card{{background:{bg_card};border:1px solid {border_card};border-radius:12px;padding:12px 14px;margin-bottom:6px;}}
.res-t{{font-size:12.5px;font-weight:700;color:{text_main};margin-bottom:3px;}}
.res-d{{font-size:11.5px;color:{text_sub};line-height:1.5;}}
.st-card{{background:{bg_card};border:1px solid {border_card};border-radius:12px;padding:12px 8px;text-align:center;}}
.st-v{{font-size:24px;font-weight:800;color:#6366F1;}}
.st-l{{font-size:10.5px;color:{text_sub};font-weight:500;margin-top:2px;}}
.set-box{{background:{bg_card};border:1px solid {border_card};border-radius:12px;padding:14px 16px;margin-bottom:10px;}}
.set-title{{font-size:13px;font-weight:700;color:{text_main};margin-bottom:10px;}}
.page-wrap{{padding:18px 24px;overflow-y:auto;height:calc(100vh - 60px);}}
.page-wrap::-webkit-scrollbar{{width:4px;}}
.page-wrap::-webkit-scrollbar-thumb{{background:{border_col};border-radius:99px;}}
</style>""", unsafe_allow_html=True)

# ── 3-Column Page Grid ────────────────────────────────────────────────────────
left, center, right = st.columns([1.15, 3.75, 1.5], gap="small")

# ╔══════════════════════════════════════════════════════╗
# ║  1. LEFT SIDEBAR                                     ║
# ╚══════════════════════════════════════════════════════╝
with left:
    # Logo & Brand Header
    st.markdown('<div class="sb-logo"><div class="sb-logo-left"><span class="sb-logo-icon">🎓</span><span class="sb-logo-text">StudyBuddy</span></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-tagline">Learn · Practice · Grow</div>', unsafe_allow_html=True)

    # Search Box (Cosmetic)
    st.markdown('<div class="sb-search-box"><span>🔍</span><input placeholder="Search topics…" disabled/><span class="sb-kbd">⌘K</span></div>', unsafe_allow_html=True)

    # Navigation Buttons
    st.markdown('<div class="sb-nav-wrap">', unsafe_allow_html=True)
    nav_items = [("💬", "Chat"), ("🧩", "Quiz Mode"), ("📚", "Study Resources"), ("📊", "Progress"), ("⚙️", "Settings")]
    for icon, label in nav_items:
        active = st.session_state.active_nav == label
        st.markdown(f'<div class="{"nav-active" if active else ""}">', unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state.active_nav = label
            if label == "Quiz Mode":
                st.session_state.mode = "Quiz Mode"
            elif label == "Chat":
                st.session_state.mode = "Study Mode"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # SDG 4 Information Card (Section 7 Specification)
    st.markdown('<div class="sb-sdg-card"><div class="sb-sdg-header"><span>4</span> QUALITY EDUCATION</div><div class="sb-sdg-title">Supporting SDG 4 — Quality Education</div><div class="sb-sdg-msg">"Better learning today, a brighter tomorrow."</div></div>', unsafe_allow_html=True)

    # AI Learning Companion Card (Section 8 Specification)
    st.markdown('<div class="sb-companion-card"><div class="sb-companion-avatar">🤖</div><div><div class="sb-companion-name">StudyBuddy Bot</div><div class="sb-companion-msg">"Your Learning Companion!"</div></div></div>', unsafe_allow_html=True)

    # Chat History List
    user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
    if user_msgs:
        st.markdown('<div class="sb-hist-label">Recent Chats</div>', unsafe_allow_html=True)
        for m in reversed(user_msgs[-3:]):
            txt = m["content"]
            preview = (txt[:30] + "…") if len(txt) > 30 else txt
            st.markdown(f'<div class="sb-hist-item">💬 {preview}</div>', unsafe_allow_html=True)

    # User Profile Card at Bottom
    status_label = "Gemini Live" if gemini_mgr.is_configured() else "Demo Mode"
    st.markdown(f'<div class="sb-user-card"><div class="sb-user-left"><div class="sb-avatar">🧑‍🎓</div><div><div class="sb-u-name">{st.session_state.profile}</div><div class="sb-u-sub">⚡ {status_label}</div></div></div></div>', unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════╗
# ║  2. CENTER MAIN CHAT AREA                            ║
# ╚══════════════════════════════════════════════════════╝
with center:
    nav = st.session_state.active_nav
    mode = st.session_state.mode
    mode_icons = {"Study Mode": "📚", "Quiz Mode": "🧩", "Exam Mode": "📝", "Explain Mode": "💡"}

    # Top Header Controls Bar (Section 9 Specification)
    tbc1, tbc2, tbc3 = st.columns([3.5, 1.4, 1])
    with tbc1:
        st.markdown(f'<div class="sb-topbar"><div class="sb-model-pill"><div class="sb-model-dot">✦</div>{mode_icons.get(mode,"🎓")} {mode} · {st.session_state.difficulty.split(" ")[0]}</div></div>', unsafe_allow_html=True)
    with tbc2:
        if st.button("＋ New Chat", key="new_chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.active_nav = "Chat"
            st.session_state.mode = "Study Mode"
            qm.initialize_quiz_session()
            st.rerun()
    with tbc3:
        t_icon = "🌙" if is_dark else "☀️"
        if st.button(f"{t_icon} Theme", key="toggle_theme", use_container_width=True):
            st.session_state.theme = "light" if is_dark else "dark"
            st.rerun()

    # Demo Mode Notice Banner
    if not gemini_mgr.is_configured():
        st.markdown('<div style="background:#EEF2FF;border-bottom:1px solid #C7D2FE;padding:7px 18px;font-size:12px;color:#3730A3;font-weight:600;display:flex;align-items:center;justify-content:space-between;"><span>⚡ <b>Demo Mode Active</b> — Instant responses enabled without API key.</span><span style="font-size:11px;opacity:.8;">Add Gemini Key in settings for live AI 🔑</span></div>', unsafe_allow_html=True)

    # ── VIEW: CHAT ────────────────────────────────────────────────────────────
    if nav == "Chat":
        if not st.session_state.messages:
            # Welcoming Hero Header Section (Section 9 Specification)
            st.markdown('<div class="sb-hero"><div class="sb-orb"></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="sb-greet">{_greeting}!</div>', unsafe_allow_html=True)
            st.markdown('<div class="sb-greet-sub">Hello! I\'m StudyBuddy 🎓📚</div>', unsafe_allow_html=True)
            st.markdown('<div class="sb-subtitle">Your AI learning tutor, here to help you understand, practice, and achieve your goals. What would you like to learn today?</div>', unsafe_allow_html=True)
            st.markdown('<div class="sb-pastel-wash"></div></div>', unsafe_allow_html=True)

            # Quick Starter Prompt Buttons
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            suggestions = [
                ("🧮", "Explain linear regression like I'm a beginner"),
                ("📘", "Give me 3 practical examples of recursion"),
                ("⚡", "What are the key formulas for Physics exam?"),
                ("🎯", "Quiz me on basic data structures"),
            ]
            s1, s2, s3, s4 = st.columns(4)
            for col, (ico, label) in zip([s1, s2, s3, s4], suggestions):
                with col:
                    if st.button(f"{ico} {label}", key=f"sugg_{label}", use_container_width=True):
                        st.session_state._injected_prompt = label
                        st.rerun()

        else:
            # Render Conversation Surface (Section 10 - 13 Specification)
            for idx, msg in enumerate(st.session_state.messages):
                is_user = msg["role"] == "user"
                with st.chat_message("user" if is_user else "assistant", avatar="🧑‍🎓" if is_user else "🎓"):
                    st.markdown(msg["content"])
                    
                    # Section 14 Specification: Learning Action Bar Pill Controls under Assistant Messages
                    if not is_user and idx == len(st.session_state.messages) - 1:
                        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                        st.markdown('<div style="font-size:11px;font-weight:700;color:#818CF8;margin-bottom:4px;">⚡ LEARNING ACTIONS:</div>', unsafe_allow_html=True)
                        act1, act2, act3, act4, act5 = st.columns(5)
                        with act1:
                            if st.button("💡 Show Example", key=f"act_ex_{idx}", use_container_width=True):
                                st.session_state._injected_prompt = f"Show me a practical example about {st.session_state.topic or eff_subj}."
                                st.rerun()
                        with act2:
                            if st.button("❓ Practice Qs", key=f"act_pq_{idx}", use_container_width=True):
                                st.session_state._injected_prompt = f"Give me 2 practice questions with answers about {st.session_state.topic or eff_subj}."
                                st.rerun()
                        with act3:
                            if st.button("🔍 In Detail", key=f"act_det_{idx}", use_container_width=True):
                                st.session_state._injected_prompt = f"Explain {st.session_state.topic or eff_subj} in more technical detail."
                                st.rerun()
                        with act4:
                            if st.button("📝 Summarize", key=f"act_sum_{idx}", use_container_width=True):
                                st.session_state._injected_prompt = f"Summarize the key takeaways for {st.session_state.topic or eff_subj} in bullet points."
                                st.rerun()
                        with act5:
                            if st.button("🐣 Make Easier", key=f"act_eas_{idx}", use_container_width=True):
                                st.session_state._injected_prompt = f"Explain {st.session_state.topic or eff_subj} in even simpler terms with an analogy."
                                st.rerun()

            # Chat Toolbar (Regenerate / Clear)
            if st.session_state.messages[-1]["role"] == "assistant":
                ra, rb, rc = st.columns([7, 0.6, 0.6])
                with rb:
                    if st.button("🔄", key="regen", help="Regenerate response"):
                        st.session_state.messages.pop()
                        if st.session_state.messages:
                            last_u = st.session_state.messages[-1]["content"]
                            resp = gemini_mgr.generate_chat_response(
                                messages=st.session_state.messages,
                                system_instruction=get_system_instruction(mode, eff_subj, st.session_state.topic, st.session_state.difficulty),
                                mode=mode, subject=eff_subj, topic=st.session_state.topic, difficulty=st.session_state.difficulty,
                            )
                            st.session_state.messages.append({"role": "assistant", "content": resp})
                        st.rerun()
                with rc:
                    if st.button("🗑️", key="del_last", help="Delete last pair"):
                        if len(st.session_state.messages) >= 2:
                            st.session_state.messages = st.session_state.messages[:-2]
                        st.rerun()

        # Handle Action Pill / Suggestion Injection
        if hasattr(st.session_state, "_injected_prompt") and st.session_state._injected_prompt:
            injected = st.session_state._injected_prompt
            del st.session_state._injected_prompt
            st.session_state.messages.append({"role": "user", "content": injected})
            st.session_state.total_messages += 1
            resp = gemini_mgr.generate_chat_response(
                messages=st.session_state.messages,
                system_instruction=get_system_instruction(mode, eff_subj, st.session_state.topic, st.session_state.difficulty),
                mode=mode, subject=eff_subj, topic=st.session_state.topic, difficulty=st.session_state.difficulty,
            )
            st.session_state.messages.append({"role": "assistant", "content": resp})
            st.rerun()

        # Real Chat Input Composer (Section 15 Specification)
        if prompt := st.chat_input(f"Ask StudyBuddy anything about {eff_subj}…"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.total_messages += 1
            tk = st.session_state.topic or eff_subj
            found = [t for t in st.session_state.recent_topics if t["name"] == tk]
            if found:
                found[0]["count"] += 1
            else:
                st.session_state.recent_topics.insert(0, {"name": tk, "count": 1})
                st.session_state.recent_topics = st.session_state.recent_topics[:6]
            
            resp = gemini_mgr.generate_chat_response(
                messages=st.session_state.messages,
                system_instruction=get_system_instruction(mode, eff_subj, st.session_state.topic, st.session_state.difficulty),
                mode=mode, subject=eff_subj, topic=st.session_state.topic, difficulty=st.session_state.difficulty,
            )
            st.session_state.messages.append({"role": "assistant", "content": resp})
            st.rerun()

        # Interactive Mode Selector Bar below Input
        st.markdown('<div class="chip-row">', unsafe_allow_html=True)
        c1, c2, c3, c4, c5 = st.columns([1.1, 1, 1.1, 0.9, 2.5])
        with c1:
            cls = "chip-active" if mode == "Study Mode" else ""
            st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
            if st.button("📚 Study", key="chip_study"):
                st.session_state.mode = "Study Mode"
                st.session_state.active_nav = "Chat"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            cls = "chip-active" if mode == "Exam Mode" else ""
            st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
            if st.button("📝 Exam", key="chip_exam"):
                st.session_state.mode = "Exam Mode"
                st.session_state.active_nav = "Chat"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c3:
            cls = "chip-active" if mode == "Explain Mode" else ""
            st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
            if st.button("💡 Explain", key="chip_explain"):
                st.session_state.mode = "Explain Mode"
                st.session_state.active_nav = "Chat"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c4:
            cls = "chip-active" if mode == "Quiz Mode" else ""
            st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
            if st.button("🧩 Quiz", key="chip_quiz"):
                st.session_state.mode = "Quiz Mode"
                st.session_state.active_nav = "Quiz Mode"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c5:
            st.markdown(f'<div style="display:flex;align-items:center;height:36px;padding-left:8px;font-size:11px;color:{text_sub};font-weight:600;">Subject: {eff_subj}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── VIEW: QUIZ MODE ───────────────────────────────────────────────────────
    elif nav == "Quiz Mode":
        st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
        qs = st.session_state.quiz_state

        if not qs["active"] or qs["subject"] != eff_subj:
            st.markdown('<div class="sb-orb" style="margin:24px auto 16px;"></div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center;font-size:24px;font-weight:800;color:{text_main};margin-bottom:6px;">Ready for Quiz Challenge?</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center;font-size:13.5px;color:{text_sub};margin-bottom:20px;line-height:1.6;">Interactive MCQs on <b>{eff_subj}</b> — test your knowledge, get instant explanations, and track your score.</div>', unsafe_allow_html=True)
            q1, q2, q3 = st.columns([2, 1.5, 2])
            with q2:
                if st.button("✦ Start Quiz Now", type="primary", use_container_width=True):
                    qm.start_new_quiz(eff_subj, st.session_state.topic, st.session_state.difficulty)
                    st.session_state.total_quizzes += 1
                    qm.fetch_next_question(gemini_mgr)
                    st.rerun()
        else:
            ha, hb = st.columns([4, 1])
            with ha:
                st.markdown(f"<h4 style='margin:0;font-weight:800;color:{text_main};'>Question {qs['question_number']}</h4>", unsafe_allow_html=True)
            with hb:
                answered = max(1, qs["question_number"] - (0 if qs["answered"] else 1))
                st.markdown(f"<div class='q-score'>🏆 {qs['score']} / {answered}</div>", unsafe_allow_html=True)
            st.progress(min(1.0, qs["question_number"] / 10.0))
            st.write("")

            if qs["current_question"]:
                q = qs["current_question"]
                st.markdown(f"<div class='quiz-q-box'>❓ {q['question']}</div>", unsafe_allow_html=True)
                opts = q.get("options", {})
                correct = q.get("correct_option", "").strip().upper()

                if not qs["answered"]:
                    sel = st.radio(
                        "Select your answer:",
                        list(opts.keys()),
                        format_func=lambda o: f"{o}.  {opts[o]}",
                        index=None,
                        key=f"q{qs['question_number']}",
                    )
                    qa1, qa2 = st.columns([1.2, 3.8])
                    with qa1:
                        if st.button("Submit Answer ✓", type="primary", use_container_width=True, disabled=sel is None):
                            if sel:
                                qm.submit_answer(sel)
                                st.rerun()
                    with qa2:
                        if q.get("hint"):
                            with st.expander("💡 View Hint"):
                                st.info(q["hint"])
                else:
                    ua = qs["user_answer"]
                    if ua == correct:
                        st.success(f"🎉 **Correct!** — {ua}: {opts.get(ua,'')}")
                        st.session_state.total_score += 1
                    else:
                        st.error(f"❌ You chose **{ua}** · Correct Answer is **{correct}:** {opts.get(correct,'')}")
                    with st.expander("📖 Explanation & Breakdown", expanded=True):
                        st.info(q.get("explanation", ""))
                    st.write("")
                    qb1, qb2, qb3 = st.columns([2, 2, 3])
                    with qb1:
                        if st.button("Next Question →", type="primary", use_container_width=True):
                            qm.fetch_next_question(gemini_mgr)
                            st.rerun()
                    with qb2:
                        if st.button("End Quiz", use_container_width=True):
                            st.info(f"**Quiz Complete!** Final Score: {qs['score']} / {qs['question_number']} 🎓")
                            qm.start_new_quiz(eff_subj, st.session_state.topic, st.session_state.difficulty)
                            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── VIEW: STUDY RESOURCES ─────────────────────────────────────────────────
    elif nav == "Study Resources":
        st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
        st.markdown(f'<div style="background:{active_bg};border-radius:10px;padding:12px 16px;margin-bottom:16px;font-size:13px;color:{active_txt};font-weight:600;">📚 Select any subject to load resources and initiate an AI tutor session.</div>', unsafe_allow_html=True)
        for icon, name, desc in [
            ("📐", "Mathematics & Statistics", "Algebra, Calculus, Probability, Linear Algebra, Differential Equations"),
            ("⚛️", "Physics", "Classical Mechanics, Thermodynamics, Electromagnetism, Quantum Physics"),
            ("🧪", "Chemistry", "Organic Chemistry, Inorganic, Physical Chemistry, Biochemistry"),
            ("💻", "Computer Science & Programming", "Algorithms, Data Structures, System Design, Operating Systems, OOP"),
            ("⚡", "Electrical & Electronics Engineering", "Circuit Analysis, Digital Logic, Microprocessors, Signal Processing"),
            ("📈", "Business & Economics", "Microeconomics, Macroeconomics, Finance, Econometrics, Management"),
            ("🧬", "Biology & Life Sciences", "Genetics, Cell Biology, Microbiology, Anatomy, Molecular Biology"),
            ("📜", "History & Social Sciences", "World History, Political Theory, Psychology, Sociology"),
        ]:
            rc1, rc2 = st.columns([4.5, 1.1])
            with rc1:
                st.markdown(f'<div class="res-card"><div class="res-t">{icon} {name}</div><div class="res-d">{desc}</div></div>', unsafe_allow_html=True)
            with rc2:
                st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                if st.button("Study →", key=f"res_{name}", use_container_width=True):
                    if name in PREDEFINED_SUBJECTS:
                        st.session_state.subject = name
                    else:
                        st.session_state.subject = "Other (Specify Below)"
                        st.session_state.custom_subject = name
                    st.session_state.mode = "Study Mode"
                    st.session_state.active_nav = "Chat"
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── VIEW: PROGRESS ────────────────────────────────────────────────────────
    elif nav == "Progress":
        st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
        hist = st.session_state.quiz_state.get("history", [])
        acc = f"{round(st.session_state.total_score / max(1, len(hist)) * 100)}%" if hist else "—"
        streak = min(len(hist), 7)
        pc1, pc2, pc3, pc4, pc5 = st.columns(5)
        for col, val, lbl in [
            (pc1, st.session_state.total_messages, "Messages"),
            (pc2, st.session_state.total_quizzes, "Quizzes"),
            (pc3, st.session_state.total_score, "Correct"),
            (pc4, acc, "Accuracy"),
            (pc5, f"🔥{streak}", "Streak"),
        ]:
            with col:
                st.markdown(f'<div class="st-card"><div class="st-v">{val}</div><div class="st-l">{lbl}</div></div>', unsafe_allow_html=True)
        st.write("")
        st.markdown(f"<h4 style='color:{text_main};font-weight:700;'>📖 Quiz History & Performance</h4>", unsafe_allow_html=True)
        if not hist:
            st.info("No quiz history recorded yet. Jump to Quiz Mode and test your knowledge!")
        else:
            for h in reversed(hist[-10:]):
                ri = "✅" if h["is_correct"] else "❌"
                q_preview = (h["question"][:85] + "…") if len(h["question"]) > 85 else h["question"]
                st.markdown(f'<div class="res-card"><div class="res-t">{ri} Q{h["question_num"]}: {q_preview}</div><div class="res-d">Your answer: <b>{h["user_answer"]}</b> · Correct: <b>{h["correct_answer"]}</b></div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── VIEW: SETTINGS ────────────────────────────────────────────────────────
    elif nav == "Settings":
        st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="set-box"><div class="set-title">🔑 Gemini API Configuration</div>', unsafe_allow_html=True)
        if api_key:
            st.success("✅ Gemini API Key is configured and active.")
            if st.button("🔄 Change API Key"):
                st.session_state.user_api_key = ""
                st.rerun()
        else:
            nk = st.text_input("Gemini API Key", type="password", placeholder="Paste key here…")
            if nk:
                st.session_state.user_api_key = nk
                st.rerun()
            st.caption("⚡ [Get a free API key at Google AI Studio →](https://aistudio.google.com/)")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="set-box"><div class="set-title">🎨 Interface & Preferences</div>', unsafe_allow_html=True)
        pm = st.selectbox("Default Mode", list(LEARNING_MODES.keys()), index=list(LEARNING_MODES.keys()).index(st.session_state.mode))
        pd = st.selectbox("Default Level", DIFFICULTY_LEVELS, index=DIFFICULTY_LEVELS.index(st.session_state.difficulty))
        if st.button("💾 Save Preferences", type="primary"):
            st.session_state.mode = pm
            st.session_state.difficulty = pd
            st.success("Saved!")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="set-box"><div class="set-title">🗑️ Reset & Clear Data</div>', unsafe_allow_html=True)
        sd1, sd2 = st.columns(2)
        with sd1:
            if st.button("Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.session_state.total_messages = 0
                st.toast("Chat cleared!", icon="🧹")
                st.rerun()
        with sd2:
            if st.button("Reset Entire Session", use_container_width=True):
                for k in ["messages", "recent_topics"]:
                    st.session_state[k] = []
                for k in ["total_messages", "total_quizzes", "total_score"]:
                    st.session_state[k] = 0
                qm.initialize_quiz_session()
                st.toast("Session reset!", icon="♻️")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════╗
# ║  3. RIGHT CONTROL PANEL                              ║
# ╚══════════════════════════════════════════════════════╝
with right:
    st.markdown('<div style="padding:14px 14px 20px;">', unsafe_allow_html=True)

    # API Key Card if missing
    if not gemini_mgr.is_configured():
        st.markdown('<div class="r-card"><div class="r-card-title">🔑 API Key (Optional)</div>', unsafe_allow_html=True)
        kv = st.text_input("k", type="password", placeholder="Paste Gemini key…", label_visibility="collapsed")
        if kv:
            st.session_state.user_api_key = kv
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Section 17 Specification: Learning Mode Card
    st.markdown('<div class="r-card"><div class="r-card-title">⚡ Learning Mode</div>', unsafe_allow_html=True)
    mk = list(LEARNING_MODES.keys())
    sm = st.selectbox(
        "Mode", mk,
        index=mk.index(st.session_state.mode),
        format_func=lambda m: f"{LEARNING_MODES[m]['icon']} {m}",
        label_visibility="collapsed",
    )
    if sm != st.session_state.mode:
        st.session_state.mode = sm
        st.session_state.active_nav = "Quiz Mode" if sm == "Quiz Mode" else "Chat"
        st.rerun()
    st.caption(LEARNING_MODES[sm]["description"])
    st.markdown("</div>", unsafe_allow_html=True)

    # Section 18 Specification: Subject / Topic Card
    st.markdown('<div class="r-card"><div class="r-card-title">📖 Subject & Topic</div>', unsafe_allow_html=True)
    ss = st.selectbox(
        "Subj", PREDEFINED_SUBJECTS,
        index=PREDEFINED_SUBJECTS.index(st.session_state.subject) if st.session_state.subject in PREDEFINED_SUBJECTS else 0,
        label_visibility="collapsed",
    )
    st.session_state.subject = ss
    if ss == "Other (Specify Below)":
        st.session_state.custom_subject = st.text_input(
            "Custom", value=st.session_state.custom_subject,
            placeholder="e.g. Quantum Computing…", label_visibility="collapsed",
        )
    st.session_state.topic = st.text_input(
        "Topic (optional)", value=st.session_state.topic,
        placeholder="e.g. Linear Regression…", label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Section 19 Specification: Learner Level Card
    st.markdown('<div class="r-card"><div class="r-card-title">📊 Learner Level</div>', unsafe_allow_html=True)
    sd = st.selectbox(
        "Diff", DIFFICULTY_LEVELS,
        index=DIFFICULTY_LEVELS.index(st.session_state.difficulty) if st.session_state.difficulty in DIFFICULTY_LEVELS else 1,
        format_func=lambda d: d.split(" ")[0],
        label_visibility="collapsed",
    )
    st.session_state.difficulty = sd
    st.caption("Adjusts the explanation depth to your level.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Section 43 Specification: Adaptive Learning Loop Component (Competition Differentiator)
    st.markdown(f'<div class="adaptive-loop-box"><div class="adaptive-loop-title"><span>🔄 ADAPTIVE LEARNING LOOP</span><span style="font-size:9.5px;background:#6366F1;color:#fff;padding:1px 5px;border-radius:4px;">ACTIVE</span></div><div class="adaptive-flow"><span class="adaptive-step">Understand</span><span class="adaptive-arrow">➔</span><span class="adaptive-step">Practice</span><span class="adaptive-arrow">➔</span><span class="adaptive-step">Adapt</span></div><div style="font-size:10.5px;color:{text_sub};margin-top:6px;line-height:1.4;">Current level: <b>{st.session_state.difficulty.split(" ")[0]}</b>. Ready for practice questions!</div></div>', unsafe_allow_html=True)

    # Section 20 Specification: Quick Actions Card
    st.markdown('<div class="r-card"><div class="r-card-title">⚡ Quick Actions</div>', unsafe_allow_html=True)
    if st.button("🧩 Start a Quiz", use_container_width=True, type="primary"):
        st.session_state.mode = "Quiz Mode"
        st.session_state.active_nav = "Quiz Mode"
        qm.start_new_quiz(eff_subj, st.session_state.topic, st.session_state.difficulty)
        st.session_state.total_quizzes += 1
        qm.fetch_next_question(gemini_mgr)
        st.rerun()
    if st.button("💡 Explain Mode", use_container_width=True):
        st.session_state.mode = "Explain Mode"
        st.session_state.active_nav = "Chat"
        st.rerun()
    if st.button("📝 Exam Mode", use_container_width=True):
        st.session_state.mode = "Exam Mode"
        st.session_state.active_nav = "Chat"
        st.rerun()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.toast("Cleared!", icon="🧹")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Section 21 Specification: Recent Topics
    if st.session_state.recent_topics:
        st.markdown('<div class="r-card"><div class="r-card-title">🕒 Recent Topics</div>', unsafe_allow_html=True)
        for t in st.session_state.recent_topics[:4]:
            st.markdown(f'<div class="tp-row"><div><div class="tp-name">{t["name"]}</div><div class="tp-cnt">{t["count"]} msg(s)</div></div><span style="color:#818CF8;font-size:12px;">›</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Section 22 Specification: SDG Footer Message Card
    st.markdown('<div style="background:linear-gradient(135deg,#ECFDF5,#D1FAE5);border:1px solid #A7F3D0;border-radius:12px;padding:12px 14px;text-align:center;font-size:11.5px;color:#065F46;font-weight:600;line-height:1.5;">Together we can make quality education accessible to everyone! 🌍</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
