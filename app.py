"""
StudyBuddy - Professional AI Learning Companion
Inspired by ChatGPT, Claude & Gemini UI patterns.
"""
import streamlit as st
from config import (
    DEFAULT_MODEL, LEARNING_MODES, PREDEFINED_SUBJECTS,
    DIFFICULTY_LEVELS, get_api_key,
)
from prompts import get_system_instruction
from gemini_client import GeminiManager, GeminiClientError
import quiz_manager as qm

st.set_page_config(
    page_title="StudyBuddy – AI Learning Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

/* ─── Reset ─── */
*,*::before,*::after{box-sizing:border-box;}
html,body{height:100vh;overflow:hidden;margin:0;padding:0;}
body,[class*="css"]{font-family:'Inter',sans-serif!important;}

/* ─── Kill Streamlit Chrome ─── */
header,#MainMenu,footer,
[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stAppDeployButton"],[data-testid="stStatusWidget"],
[data-testid="collapsedControl"]{display:none!important;}

/* ─── Full-Height App Shell ─── */
.stApp{height:100vh!important;overflow:hidden!important;background:#F7F8FC!important;}
.block-container{padding:0!important;max-width:100vw!important;height:100vh!important;overflow:hidden!important;}
[data-testid="stMainBlockContainer"]{padding:0!important;height:100vh!important;overflow:hidden!important;}
section[data-testid="stMain"]{height:100vh!important;overflow:hidden!important;}
section[data-testid="stMain"]>div:first-child{padding:0!important;height:100%!important;}
[data-testid="stHorizontalBlock"]{gap:0!important;align-items:stretch!important;height:100vh!important;}
[data-testid="column"]{padding:0!important;height:100vh!important;}
[data-testid="stVerticalBlock"]{gap:0!important;}
.stMarkdown{margin:0!important;}

/* ══════════ LEFT SIDEBAR ══════════ */
[data-testid="column"]:nth-child(1){
    background:#1C1C2E!important;
    border-right:none!important;
    height:100vh!important;
    overflow-y:auto!important;
    overflow-x:hidden!important;
}
[data-testid="column"]:nth-child(1)::-webkit-scrollbar{display:none;}

/* Logo */
.sb-logo{
    display:flex;align-items:center;gap:10px;
    padding:22px 16px 18px;
    border-bottom:1px solid rgba(255,255,255,0.07);
}
.sb-logo-icon{
    width:38px;height:38px;
    background:linear-gradient(135deg,#6366F1,#8B5CF6);
    border-radius:10px;
    display:flex;align-items:center;justify-content:center;
    font-size:18px;flex-shrink:0;
    box-shadow:0 4px 14px rgba(99,102,241,0.4);
}
.sb-logo-title{font-size:15px;font-weight:800;color:#fff;line-height:1.2;}
.sb-logo-tag{font-size:9.5px;color:rgba(255,255,255,0.4);font-weight:500;letter-spacing:0.05em;}

/* Nav Buttons */
[data-testid="column"]:nth-child(1) .stButton>button{
    width:100%!important;
    text-align:left!important;
    justify-content:flex-start!important;
    padding:9px 12px!important;
    font-size:13.5px!important;
    font-weight:500!important;
    border-radius:8px!important;
    border:none!important;
    background:transparent!important;
    color:rgba(255,255,255,0.55)!important;
    box-shadow:none!important;
    margin:1px 0!important;
    transition:all 0.15s ease!important;
    letter-spacing:0.01em!important;
}
[data-testid="column"]:nth-child(1) .stButton>button:hover{
    background:rgba(255,255,255,0.07)!important;
    color:rgba(255,255,255,0.9)!important;
}
.nav-active .stButton>button{
    background:rgba(99,102,241,0.18)!important;
    color:#A5B4FC!important;
    box-shadow:inset 3px 0 0 #6366F1!important;
    border-radius:0 8px 8px 0!important;
}
.nav-active .stButton>button:hover{
    background:rgba(99,102,241,0.25)!important;
    color:#C7D2FE!important;
}
.nav-area{padding:10px 4px;}

/* User info at bottom of sidebar */
.sb-user-area{
    position:absolute;bottom:0;left:0;right:0;
    background:#1C1C2E;
    border-top:1px solid rgba(255,255,255,0.07);
    padding:14px 16px;
}
.sb-user-pill{
    display:flex;align-items:center;gap:10px;
}
.sb-user-avatar{
    width:32px;height:32px;
    background:linear-gradient(135deg,#6366F1,#8B5CF6);
    border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    font-size:14px;flex-shrink:0;
}
.sb-user-name{font-size:12px;font-weight:600;color:rgba(255,255,255,0.8);}
.sb-user-sub{font-size:10px;color:rgba(255,255,255,0.35);}

/* SDG badge in sidebar */
.sb-sdg-mini{
    margin:10px 8px;
    padding:12px;
    background:linear-gradient(135deg,rgba(99,102,241,0.15),rgba(139,92,246,0.1));
    border-radius:10px;
    border:1px solid rgba(99,102,241,0.25);
}
.sb-sdg-mini .num{
    display:inline-flex;align-items:center;justify-content:center;
    width:28px;height:28px;
    background:linear-gradient(135deg,#DC2626,#B91C1C);
    border-radius:6px;
    font-size:13px;font-weight:800;color:#fff;margin-bottom:6px;
}
.sb-sdg-mini .t1{font-size:11px;font-weight:700;color:#A5B4FC;margin-bottom:2px;}
.sb-sdg-mini .t2{font-size:10.5px;color:rgba(165,180,252,0.6);line-height:1.4;}

/* ══════════ CENTER CHAT AREA ══════════ */
[data-testid="column"]:nth-child(2){
    background:#F7F8FC!important;
    height:100vh!important;
    display:flex!important;
    flex-direction:column!important;
    overflow:hidden!important;
}
[data-testid="column"]:nth-child(2)>[data-testid="stVerticalBlock"]{
    height:100vh!important;
    display:flex!important;
    flex-direction:column!important;
    overflow:hidden!important;
}

/* Top bar */
.sb-topbar{
    display:flex;align-items:center;justify-content:space-between;
    padding:14px 24px 13px;
    background:#fff;
    border-bottom:1px solid #EAECF2;
    flex-shrink:0;
    box-shadow:0 1px 3px rgba(0,0,0,0.04);
}
.sb-topbar-left{display:flex;align-items:center;gap:10px;}
.sb-topbar-title{font-size:15px;font-weight:700;color:#111827;}
.sb-topbar-sub{font-size:12px;color:#9CA3AF;font-weight:400;}
.sb-topbar-badge{
    display:inline-flex;align-items:center;gap:5px;
    background:#EEF2FF;color:#4F46E5;
    border-radius:20px;padding:3px 10px;
    font-size:11.5px;font-weight:600;
    border:1px solid #C7D2FE;
}
.sb-online-dot{
    width:7px;height:7px;
    background:#22C55E;border-radius:50%;
    display:inline-block;
    box-shadow:0 0 0 2px rgba(34,197,94,0.2);
    animation:pulse 2s infinite;
}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.5;}}

/* API key warning bar */
.sb-api-bar{
    background:#FFFBEB;border-bottom:1px solid #FDE68A;
    padding:8px 24px;
    font-size:12.5px;color:#92400E;font-weight:500;
    flex-shrink:0;display:flex;align-items:center;gap:8px;
}

/* ── Chat messages ── */
[data-testid="stChatMessageContainer"]{
    flex:1!important;
    overflow-y:auto!important;
    padding:16px 0!important;
}
[data-testid="stChatMessageContainer"]::-webkit-scrollbar{width:4px;}
[data-testid="stChatMessageContainer"]::-webkit-scrollbar-thumb{background:#D1D5DB;border-radius:99px;}

[data-testid="stChatMessage"]{background:transparent!important;padding:2px 24px!important;}

/* User message */
[data-testid="stChatMessage"][data-testid*="user"],
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]){
    flex-direction:row-reverse!important;
}

/* AI bubble gets a white card look */
[data-testid="stChatMessageContent"]{
    font-size:14px!important;
    line-height:1.75!important;
    color:#111827!important;
}

/* Chat input area */
[data-testid="stBottom"]{
    background:#F7F8FC!important;
    padding:0 24px 16px!important;
    border-top:1px solid #EAECF2!important;
    flex-shrink:0!important;
}
[data-testid="stChatInput"]{
    background:#fff!important;
    border:1.5px solid #E5E7EB!important;
    border-radius:14px!important;
    font-size:14px!important;
    box-shadow:0 2px 8px rgba(0,0,0,0.05)!important;
    transition:border-color 0.2s,box-shadow 0.2s!important;
}
[data-testid="stChatInput"]:focus-within{
    border-color:#6366F1!important;
    box-shadow:0 2px 16px rgba(99,102,241,0.12)!important;
}

/* Suggested prompts */
.sb-prompt-grid{
    display:flex;flex-wrap:wrap;gap:8px;
    padding:0 24px 12px;
}
.sb-prompt-chip{
    background:#fff;
    border:1px solid #E5E7EB;
    border-radius:20px;
    padding:7px 14px;
    font-size:12.5px;
    color:#374151;
    font-weight:500;
    cursor:pointer;
    transition:all 0.15s ease;
    white-space:nowrap;
}
.sb-prompt-chip:hover{background:#EEF2FF;border-color:#C7D2FE;color:#4F46E5;}

/* Welcome screen */
.sb-welcome-screen{
    flex:1;
    display:flex;flex-direction:column;
    align-items:center;justify-content:center;
    padding:32px 40px;
    min-height:0;
}
.sb-welcome-icon{font-size:56px;margin-bottom:16px;line-height:1;}
.sb-welcome-h1{font-size:26px;font-weight:800;color:#111827;margin-bottom:8px;text-align:center;}
.sb-welcome-h1 span{color:#6366F1;}
.sb-welcome-p{font-size:14px;color:#6B7280;line-height:1.7;text-align:center;max-width:440px;margin-bottom:24px;}
.sb-mode-chips{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-bottom:28px;}
.sb-mode-chip{
    display:inline-flex;align-items:center;gap:6px;
    background:#fff;border:1px solid #E5E7EB;
    border-radius:20px;padding:7px 14px;
    font-size:12.5px;font-weight:600;color:#374151;
}
.sb-suggestion-grid{
    display:grid;grid-template-columns:1fr 1fr;gap:10px;width:100%;max-width:560px;
}
.sb-suggestion-card{
    background:#fff;
    border:1px solid #E5E7EB;
    border-radius:12px;
    padding:14px 16px;
    cursor:pointer;
    transition:all 0.18s ease;
    text-align:left;
}
.sb-suggestion-card:hover{border-color:#C7D2FE;background:#F5F3FF;box-shadow:0 4px 12px rgba(99,102,241,0.1);}
.sb-suggestion-card .sc-icon{font-size:20px;margin-bottom:6px;}
.sb-suggestion-card .sc-title{font-size:13px;font-weight:700;color:#111827;margin-bottom:2px;}
.sb-suggestion-card .sc-desc{font-size:12px;color:#9CA3AF;}

/* ══════════ RIGHT PANEL ══════════ */
[data-testid="column"]:nth-child(3){
    background:#fff!important;
    border-left:1px solid #EAECF2!important;
    height:100vh!important;
    overflow-y:auto!important;
    overflow-x:hidden!important;
}
[data-testid="column"]:nth-child(3)::-webkit-scrollbar{width:3px;}
[data-testid="column"]:nth-child(3)::-webkit-scrollbar-thumb{background:#E5E7EB;border-radius:99px;}

/* Right panel widgets */
[data-testid="column"]:nth-child(3) .stButton>button{
    border-radius:9px!important;
    font-size:12.5px!important;
    font-weight:600!important;
    border:1px solid #E5E7EB!important;
    background:#F9FAFB!important;
    color:#374151!important;
    transition:all 0.15s!important;
    padding:8px 12px!important;
}
[data-testid="column"]:nth-child(3) .stButton>button:hover{
    background:#EEF2FF!important;
    border-color:#C7D2FE!important;
    color:#4F46E5!important;
}
[data-testid="column"]:nth-child(3) .stButton>button[kind="primary"]{
    background:linear-gradient(135deg,#6366F1,#8B5CF6)!important;
    color:#fff!important;border:none!important;
    box-shadow:0 4px 12px rgba(99,102,241,0.3)!important;
}
[data-testid="column"]:nth-child(3) .stButton>button[kind="primary"]:hover{
    box-shadow:0 6px 18px rgba(99,102,241,0.4)!important;
    transform:translateY(-1px)!important;
}
[data-testid="column"]:nth-child(3) div[data-testid="stSelectbox"]>div>div{
    background:#F9FAFB!important;border:1px solid #E5E7EB!important;
    border-radius:9px!important;font-size:13px!important;
}
[data-testid="column"]:nth-child(3) div[data-testid="stTextInput"] input{
    background:#F9FAFB!important;border:1px solid #E5E7EB!important;
    border-radius:9px!important;font-size:13px!important;
}
[data-testid="column"]:nth-child(3) div[data-testid="stSelectbox"] label,
[data-testid="column"]:nth-child(3) div[data-testid="stTextInput"] label{
    font-size:11.5px!important;font-weight:600!important;color:#6B7280!important;
    text-transform:uppercase!important;letter-spacing:0.04em!important;
}
.r-section{padding:14px 14px 0;}
.r-head{font-size:11px;font-weight:700;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;}
hr.r-div{border:none;border-top:1px solid #F3F4F6;margin:12px 0;}

/* Topic pill */
.topic-pill{
    display:flex;align-items:center;justify-content:space-between;
    padding:8px 10px;border-radius:8px;
    background:#F9FAFB;border:1px solid #F3F4F6;
    margin-bottom:5px;cursor:pointer;transition:all 0.15s;
}
.topic-pill:hover{background:#EEF2FF;border-color:#C7D2FE;}
.topic-pill .tp-name{font-size:12.5px;font-weight:600;color:#374151;}
.topic-pill .tp-cnt{font-size:11px;color:#9CA3AF;}
.topic-pill .tp-arr{font-size:12px;color:#D1D5DB;}

/* SDG note */
.r-sdg-note{
    margin:10px 14px 14px;
    background:linear-gradient(135deg,#ECFDF5,#D1FAE5);
    border:1px solid #A7F3D0;
    border-radius:10px;padding:12px 13px;
    font-size:11.5px;color:#065F46;font-weight:500;
    line-height:1.6;text-align:center;
}

/* ── Quiz styling ── */
.quiz-q{
    background:#fff;border:1px solid #E5E7EB;
    border-left:4px solid #6366F1;border-radius:12px;
    padding:16px 20px;font-size:14.5px;font-weight:600;
    color:#111827;margin-bottom:14px;line-height:1.5;
    box-shadow:0 2px 8px rgba(0,0,0,0.04);
}
.quiz-score{
    display:inline-flex;align-items:center;gap:5px;
    background:#EEF2FF;color:#4F46E5;
    padding:5px 13px;border-radius:20px;
    font-size:12.5px;font-weight:700;border:1px solid #C7D2FE;
}

/* ── Resource card ── */
.res-card{
    background:#fff;border:1px solid #E5E7EB;
    border-radius:12px;padding:14px 16px;margin-bottom:6px;
    box-shadow:0 1px 4px rgba(0,0,0,0.03);
    transition:all 0.18s ease;
}
.res-card:hover{border-color:#C7D2FE;box-shadow:0 4px 12px rgba(99,102,241,0.08);}
.res-card-t{font-size:13.5px;font-weight:700;color:#111827;margin-bottom:3px;}
.res-card-d{font-size:12px;color:#6B7280;line-height:1.5;}

/* ── Progress stat ── */
.stat-card{
    background:#fff;border:1px solid #E5E7EB;
    border-radius:12px;padding:14px 10px;text-align:center;
    box-shadow:0 1px 4px rgba(0,0,0,0.03);
}
.stat-card .sv{font-size:26px;font-weight:800;color:#6366F1;}
.stat-card .sl{font-size:11.5px;color:#6B7280;font-weight:500;margin-top:3px;}

/* ── Settings box ── */
.set-box{
    background:#fff;border:1px solid #E5E7EB;
    border-radius:12px;padding:16px 18px;margin-bottom:10px;
}
.set-title{font-size:14px;font-weight:700;color:#111827;margin-bottom:12px;}

/* Page content padding */
.page-body{padding:20px 28px;overflow-y:auto;}
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
api_key    = get_api_key(st.session_state.user_api_key)
gemini_mgr = GeminiManager(api_key=api_key)
eff_subj   = (
    st.session_state.custom_subject
    if st.session_state.subject == "Other (Specify Below)" and st.session_state.custom_subject.strip()
    else st.session_state.subject
)

# ── 3-Column Layout ───────────────────────────────────────────────────────────
left, center, right = st.columns([1.05, 3.85, 1.55], gap="small")

# ╔══════════════════════════════════════════════════════╗
# ║  LEFT SIDEBAR (dark)                                 ║
# ╚══════════════════════════════════════════════════════╝
with left:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-icon">🎓</div>
        <div>
            <div class="sb-logo-title">StudyBuddy</div>
            <div class="sb-logo-tag">LEARN · PRACTICE · GROW</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-area">', unsafe_allow_html=True)
    for icon, label in [("💬","Chat"),("🧩","Quiz Mode"),("📚","Study Resources"),("📊","Progress"),("⚙️","Settings")]:
        active = st.session_state.active_nav == label
        st.markdown(f'<div class="{"nav-active" if active else "nav-inactive"}">', unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state.active_nav = label
            if label == "Chat": st.session_state.mode = "Study Mode"
            elif label == "Quiz Mode": st.session_state.mode = "Quiz Mode"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-sdg-mini">
        <div class="num">4</div>
        <div class="t1">SDG 4 – Quality Education</div>
        <div class="t2">AI-powered learning for everyone, everywhere.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:10px 8px 6px;">
        <div class="sb-user-pill">
            <div class="sb-user-avatar">🧑‍🎓</div>
            <div>
                <div class="sb-user-name">Student</div>
                <div class="sb-user-sub">Free Plan · Gemini Powered</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════╗
# ║  CENTER PANEL                                        ║
# ╚══════════════════════════════════════════════════════╝
with center:
    nav = st.session_state.active_nav
    mode_icon_map = {"Study Mode":"📚","Quiz Mode":"🧩","Exam Mode":"📝","Explain Mode":"💡"}

    # ── Top Bar ────────────────────────────────────────────────────────────────
    topbar_map = {
        "Chat":            (f"{mode_icon_map.get(st.session_state.mode,'📚')} {st.session_state.mode}", eff_subj),
        "Quiz Mode":       ("🧩 Quiz Mode", f"MCQ · {eff_subj}"),
        "Study Resources": ("📚 Study Resources", "All Subjects"),
        "Progress":        ("📊 Progress Dashboard", "Your Stats"),
        "Settings":        ("⚙️ Settings", "Preferences"),
    }
    tb_title, tb_sub = topbar_map.get(nav, ("StudyBuddy", ""))
    st.markdown(f"""
    <div class="sb-topbar">
        <div class="sb-topbar-left">
            <div>
                <div class="sb-topbar-title">{tb_title}</div>
                <div class="sb-topbar-sub">{tb_sub}</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;">
            <span class="sb-topbar-badge">
                <span class="sb-online-dot"></span> AI Online
            </span>
            <span style="font-size:12px;color:#9CA3AF;font-weight:500;">{st.session_state.difficulty.split(' ')[0]}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # API key bar
    if not gemini_mgr.is_configured():
        st.markdown('<div class="sb-api-bar">🔑 <strong>API Key required</strong> — paste your Gemini key in the right panel. <a href="https://aistudio.google.com/" target="_blank" style="color:#78350F;text-decoration:underline;">Get a free key →</a></div>', unsafe_allow_html=True)

    # ── CHAT ──────────────────────────────────────────────────────────────────
    if nav == "Chat":
        suggestions = {
            "Study Mode":  [("🧮","Explain this concept","Explain recursion with a real-world analogy"),
                            ("📘","Give me examples","Show me 3 examples of polymorphism in OOP"),
                            ("🔍","Deep dive","What are the key differences between TCP and UDP?"),
                            ("✅","Check my understanding","Quiz me on Big-O notation basics")],
            "Exam Mode":   [("📝","Key formulas","List all important integration formulas"),
                            ("⚠️","Common mistakes","What are the top 5 mistakes in calculus exams?"),
                            ("🏆","Model answer","Write a model answer for: What is the OSI model?"),
                            ("📌","High-yield topics","What are the highest-yield topics for DBMS exams?")],
            "Explain Mode":[("🎯","Simple analogy","Explain machine learning like I'm 10"),
                            ("🏫","College level","Explain gradient descent at college standard"),
                            ("🚀","Advanced","Explain transformer attention mechanism deeply"),
                            ("🔄","All 3 levels","Explain neural networks at all 3 levels")],
        }

        if not st.session_state.messages:
            mode = st.session_state.mode
            mode_desc = {
                "Study Mode":  "Ask me anything — I'll break it down with examples, analogies, and step-by-step explanations.",
                "Exam Mode":   "Exam prep mode: high-yield content, model answers, common mistakes & last-minute revision.",
                "Explain Mode":"Every concept at 3 levels: Simple Analogy → College Standard → Advanced Insight.",
            }
            chips_html = "".join(
                f'<span class="sb-mode-chip">{icon_m} {m.replace(" Mode","")}</span>'
                for icon_m, m in [("📚","Study Mode"),("📝","Exam Mode"),("💡","Explain Mode"),("🧩","Quiz Mode")]
            )
            st.markdown(f"""
            <div class="sb-welcome-screen">
                <div class="sb-welcome-icon">✨</div>
                <div class="sb-welcome-h1">Hello! I'm <span>StudyBuddy</span></div>
                <div class="sb-welcome-p">{mode_desc.get(mode,"Your AI learning companion.")}</div>
                <div class="sb-mode-chips">{chips_html}</div>
                <div class="sb-suggestion-grid">
            """, unsafe_allow_html=True)

            sugg = suggestions.get(mode, suggestions["Study Mode"])
            for s_ico, s_title, s_desc in sugg:
                st.markdown(f"""
                <div class="sb-suggestion-card">
                    <div class="sc-icon">{s_ico}</div>
                    <div class="sc-title">{s_title}</div>
                    <div class="sc-desc">{s_desc}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)

        # Messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="🧑‍🎓" if msg["role"] == "user" else "🤖"):
                st.markdown(msg["content"])

        # Suggested prompt chips above input
        if not st.session_state.messages:
            pass  # shown inside welcome screen
        else:
            # Show regenerate option after last AI msg
            if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
                c1, c2, c3 = st.columns([6, 1, 1])
                with c2:
                    if st.button("🔄", help="Regenerate response", key="regen"):
                        last_user = next((m for m in reversed(st.session_state.messages) if m["role"] == "user"), None)
                        if last_user and gemini_mgr.is_configured():
                            st.session_state.messages.pop()
                            with st.spinner("Regenerating..."):
                                try:
                                    resp = gemini_mgr.generate_chat_response(
                                        messages=st.session_state.messages,
                                        system_instruction=get_system_instruction(
                                            mode=st.session_state.mode, subject=eff_subj,
                                            topic=st.session_state.topic, difficulty=st.session_state.difficulty,
                                        ),
                                        model_name=DEFAULT_MODEL,
                                    )
                                    st.session_state.messages.append({"role": "assistant", "content": resp})
                                except Exception: pass
                            st.rerun()
                with c3:
                    if st.button("🗑️", help="Clear chat", key="clr"):
                        st.session_state.messages = []
                        st.rerun()

        # Chat input
        if prompt := st.chat_input(f"Ask StudyBuddy anything about {eff_subj}..."):
            if not gemini_mgr.is_configured():
                st.error("🔑 Add your Gemini API key in the right panel.")
            else:
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.total_messages += 1
                tk = st.session_state.topic or eff_subj
                found = [t for t in st.session_state.recent_topics if t["name"] == tk]
                if found: found[0]["count"] += 1
                else:
                    st.session_state.recent_topics.insert(0, {"name": tk, "count": 1})
                    st.session_state.recent_topics = st.session_state.recent_topics[:6]

                with st.chat_message("user", avatar="🧑‍🎓"):
                    st.markdown(prompt)
                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner(""):
                        try:
                            resp = gemini_mgr.generate_chat_response(
                                messages=st.session_state.messages,
                                system_instruction=get_system_instruction(
                                    mode=st.session_state.mode, subject=eff_subj,
                                    topic=st.session_state.topic, difficulty=st.session_state.difficulty,
                                ),
                                model_name=DEFAULT_MODEL,
                            )
                            st.markdown(resp)
                            st.session_state.messages.append({"role": "assistant", "content": resp})
                        except GeminiClientError as e: st.error(str(e))
                        except Exception as e: st.error(f"Error: {e}")

    # ── QUIZ ──────────────────────────────────────────────────────────────────
    elif nav == "Quiz Mode":
        qs = st.session_state.quiz_state
        st.markdown('<div class="page-body">', unsafe_allow_html=True)

        if not qs["active"] or qs["subject"] != eff_subj:
            st.markdown(f"""
            <div style="max-width:520px;margin:32px auto;">
                <div class="sb-welcome-icon" style="text-align:center;font-size:52px;">🧩</div>
                <div class="sb-welcome-h1" style="text-align:center;font-size:22px;margin-top:12px;">Ready to be Tested?</div>
                <div class="sb-welcome-p" style="text-align:center;">AI-generated MCQs on <strong>{eff_subj}</strong> — 
                one question at a time with instant feedback, explanations, and live scoring.</div>
                <div style="text-align:center;margin-top:4px;">
                    <span class="sb-topbar-badge">Topic: {st.session_state.topic or 'All Topics'}</span>
                    &nbsp;
                    <span class="sb-topbar-badge">{st.session_state.difficulty.split(' ')[0]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            c1,c2,c3 = st.columns([2,1.4,2])
            with c2:
                if st.button("🚀 Start Quiz", type="primary", use_container_width=True, disabled=not gemini_mgr.is_configured()):
                    qm.start_new_quiz(eff_subj, st.session_state.topic, st.session_state.difficulty)
                    st.session_state.total_quizzes += 1
                    with st.spinner("Generating question..."): qm.fetch_next_question(gemini_mgr)
                    st.rerun()
        else:
            ca, cb = st.columns([4,1])
            with ca:
                st.markdown(f"<h4 style='margin:0;color:#111827;font-weight:700;'>Question {qs['question_number']}</h4>", unsafe_allow_html=True)
            with cb:
                answered = max(1, qs["question_number"] - (0 if qs["answered"] else 1))
                st.markdown(f"<div class='quiz-score'>🏆 {qs['score']} / {answered}</div>", unsafe_allow_html=True)
            st.progress(min(1.0, qs["question_number"] / 10.0))
            st.write("")

            if qs["error_msg"]:
                st.error(qs["error_msg"])
                if st.button("🔄 Retry"):
                    with st.spinner(): qm.fetch_next_question(gemini_mgr)
                    st.rerun()
            elif qs["current_question"]:
                q = qs["current_question"]
                st.markdown(f"<div class='quiz-q'>❓ {q['question']}</div>", unsafe_allow_html=True)
                opts = q.get("options", {})
                correct = q.get("correct_option","").strip().upper()

                if not qs["answered"]:
                    sel = st.radio("Choose:", list(opts.keys()),
                                   format_func=lambda o: f"  {o}.  {opts[o]}", index=None,
                                   key=f"q{qs['question_number']}")
                    c1,c2 = st.columns([1,4])
                    with c1:
                        if st.button("✅ Submit", type="primary", use_container_width=True, disabled=sel is None):
                            if sel: qm.submit_answer(sel); st.rerun()
                    with c2:
                        if q.get("hint"):
                            with st.expander("💡 Show Hint"): st.info(q["hint"])
                else:
                    ua = qs["user_answer"]
                    if ua == correct:
                        st.success(f"🎉 **Correct!** — **{ua}:** {opts.get(ua,'')}")
                    else:
                        st.error(f"❌ You chose **{ua}** | Correct: **{correct}:** {opts.get(correct,'')}")
                    with st.expander("📖 Full Explanation", expanded=True):
                        st.info(q.get("explanation",""))
                    st.write("")
                    c1,c2,c3 = st.columns([2,2,3])
                    with c1:
                        if st.button("➡️ Next", type="primary", use_container_width=True):
                            with st.spinner(): qm.fetch_next_question(gemini_mgr)
                            st.rerun()
                    with c2:
                        if st.button("🏁 End Quiz", use_container_width=True):
                            st.info(f"**Quiz Complete!** Final Score: **{qs['score']} / {qs['question_number']}** 🎓")
                            qm.start_new_quiz(eff_subj, st.session_state.topic, st.session_state.difficulty)
                            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── STUDY RESOURCES ───────────────────────────────────────────────────────
    elif nav == "Study Resources":
        st.markdown('<div class="page-body">', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#EEF2FF;border-radius:10px;padding:12px 16px;margin-bottom:18px;font-size:13px;color:#4F46E5;font-weight:600;">
            💡 Click <strong>Study →</strong> on any subject to load it and start a focused AI chat session.
        </div>""", unsafe_allow_html=True)
        resources = [
            ("📐","Mathematics & Statistics","Algebra, Calculus, Probability, Statistics, Linear Algebra, Discrete Maths"),
            ("⚛️","Physics","Mechanics, Thermodynamics, Electromagnetism, Quantum Physics, Optics"),
            ("🧪","Chemistry","Organic, Inorganic, Physical Chemistry, Electrochemistry, Thermochemistry"),
            ("💻","Computer Science & Programming","DSA, Algorithms, OS, DBMS, Networks, OOP, System Design"),
            ("⚡","Electronics & Electrical Engineering","Circuits, Digital Electronics, Microprocessors, Control Systems"),
            ("📈","Business & Economics","Micro/Macro Economics, Finance, Marketing, Management, Statistics"),
            ("🧬","Biology & Life Sciences","Cell Biology, Genetics, Ecology, Biochemistry, Physiology"),
            ("📜","History & Social Sciences","World History, Political Science, Sociology, Geography, Psychology"),
        ]
        for icon, name, desc in resources:
            c1,c2 = st.columns([4.5,1])
            with c1:
                st.markdown(f'<div class="res-card"><div class="res-card-t">{icon} {name}</div><div class="res-card-d">{desc}</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
                if st.button("Study →", key=f"r_{name}", use_container_width=True):
                    if name in PREDEFINED_SUBJECTS: st.session_state.subject = name
                    else:
                        st.session_state.subject = "Other (Specify Below)"
                        st.session_state.custom_subject = name
                    st.session_state.mode = "Study Mode"
                    st.session_state.active_nav = "Chat"
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── PROGRESS ──────────────────────────────────────────────────────────────
    elif nav == "Progress":
        st.markdown('<div class="page-body">', unsafe_allow_html=True)
        hist  = st.session_state.quiz_state.get("history", [])
        acc   = f"{round(st.session_state.total_score/max(1,len(hist))*100)}%" if hist else "—"
        streak = min(len(hist), 5)
        c1,c2,c3,c4,c5 = st.columns(5)
        for col,val,lbl in [
            (c1, st.session_state.total_messages, "Messages"),
            (c2, st.session_state.total_quizzes,  "Quizzes"),
            (c3, st.session_state.total_score,    "Correct"),
            (c4, acc,                             "Accuracy"),
            (c5, f"🔥{streak}",                  "Streak"),
        ]:
            with col:
                st.markdown(f'<div class="stat-card"><div class="sv">{val}</div><div class="sl">{lbl}</div></div>', unsafe_allow_html=True)
        st.write("")
        st.markdown("#### 📖 Quiz History")
        if not hist:
            st.info("No quiz history yet. Start a quiz to see your results here!")
        else:
            for h in reversed(hist[-12:]):
                ri = "✅" if h["is_correct"] else "❌"
                st.markdown(f"""
                <div class="res-card">
                    <div class="res-card-t">{ri} Q{h['question_num']}: {h['question'][:90]}{'...' if len(h['question'])>90 else ''}</div>
                    <div class="res-card-d">Your answer: <strong>{h['user_answer']}</strong> &nbsp;|&nbsp; Correct: <strong>{h['correct_answer']}</strong></div>
                </div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("#### 💬 Topics Studied")
        if not st.session_state.recent_topics:
            st.info("Start chatting to track your topics!")
        else:
            for t in st.session_state.recent_topics:
                st.markdown(f"""
                <div class="topic-pill">
                    <div><div class="tp-name">{t['name']}</div><div class="tp-cnt">{t['count']} msg(s)</div></div>
                    <div class="tp-arr">›</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── SETTINGS ──────────────────────────────────────────────────────────────
    elif nav == "Settings":
        st.markdown('<div class="page-body">', unsafe_allow_html=True)
        st.markdown('<div class="set-box"><div class="set-title">🔑 Gemini API Key</div>', unsafe_allow_html=True)
        if api_key:
            st.success("✅ API Key is active and configured.")
            if st.button("🔄 Change API Key"):
                st.session_state.user_api_key = ""; st.rerun()
        else:
            nk = st.text_input("API Key", type="password", placeholder="Paste your Gemini API key here...")
            if nk: st.session_state.user_api_key = nk; st.rerun()
            st.caption("[Get a free key at Google AI Studio →](https://aistudio.google.com/)")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="set-box"><div class="set-title">🎨 Learning Preferences</div>', unsafe_allow_html=True)
        pm = st.selectbox("Default Learning Mode", list(LEARNING_MODES.keys()),
                          index=list(LEARNING_MODES.keys()).index(st.session_state.mode))
        pd = st.selectbox("Default Difficulty", DIFFICULTY_LEVELS,
                          index=DIFFICULTY_LEVELS.index(st.session_state.difficulty))
        if st.button("💾 Save Preferences", type="primary"):
            st.session_state.mode = pm; st.session_state.difficulty = pd
            st.success("✅ Saved!")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="set-box"><div class="set-title">🗑️ Data Management</div>', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []; st.session_state.total_messages = 0
                st.toast("Chat cleared!", icon="🧹"); st.rerun()
        with c2:
            if st.button("♻️ Reset All", use_container_width=True):
                for k in ["messages","recent_topics"]: st.session_state[k] = []
                for k in ["total_messages","total_quizzes","total_score"]: st.session_state[k] = 0
                qm.initialize_quiz_session()
                st.toast("All data reset!", icon="♻️"); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="set-box"><div class="set-title">ℹ️ About</div>', unsafe_allow_html=True)
        st.markdown("""
        **StudyBuddy v1.0** — AI-powered learning for college students.
        
        Built with Python + Streamlit + Google Gemini API.
        SDG Alignment: **Goal 4 — Quality Education** 🌱
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════╗
# ║  RIGHT PANEL                                         ║
# ╚══════════════════════════════════════════════════════╝
with right:
    st.markdown('<div style="padding:16px 14px 20px;">', unsafe_allow_html=True)

    if not gemini_mgr.is_configured():
        st.markdown('<div class="r-head">🔑 API KEY</div>', unsafe_allow_html=True)
        kv = st.text_input("k", type="password", placeholder="Paste Gemini API key...", label_visibility="collapsed")
        if kv: st.session_state.user_api_key = kv; st.rerun()
        st.markdown('<hr class="r-div"/>', unsafe_allow_html=True)

    st.markdown('<div class="r-head">⚡ LEARNING MODE</div>', unsafe_allow_html=True)
    mk = list(LEARNING_MODES.keys())
    sm = st.selectbox("Mode", mk,
                      index=mk.index(st.session_state.mode),
                      format_func=lambda m: f"{LEARNING_MODES[m]['icon']} {m}",
                      label_visibility="collapsed")
    if sm != st.session_state.mode:
        st.session_state.mode = sm
        st.session_state.active_nav = "Quiz Mode" if sm == "Quiz Mode" else "Chat"
        st.rerun()
    st.caption(LEARNING_MODES[sm]["description"])
    st.markdown('<hr class="r-div"/>', unsafe_allow_html=True)

    st.markdown('<div class="r-head">📖 SUBJECT</div>', unsafe_allow_html=True)
    ss = st.selectbox("Subj", PREDEFINED_SUBJECTS,
                      index=PREDEFINED_SUBJECTS.index(st.session_state.subject) if st.session_state.subject in PREDEFINED_SUBJECTS else 0,
                      label_visibility="collapsed")
    st.session_state.subject = ss
    if ss == "Other (Specify Below)":
        st.session_state.custom_subject = st.text_input("Custom", value=st.session_state.custom_subject,
                                                         placeholder="e.g. Quantum Computing...", label_visibility="collapsed")
    st.markdown('<div class="r-head" style="margin-top:6px;">📌 TOPIC</div>', unsafe_allow_html=True)
    st.session_state.topic = st.text_input("Topic", value=st.session_state.topic,
                                            placeholder="e.g. Sorting Algorithms...", label_visibility="collapsed")
    st.markdown('<hr class="r-div"/>', unsafe_allow_html=True)

    st.markdown('<div class="r-head">📊 LEARNER LEVEL</div>', unsafe_allow_html=True)
    sd = st.selectbox("Diff", DIFFICULTY_LEVELS,
                      index=DIFFICULTY_LEVELS.index(st.session_state.difficulty) if st.session_state.difficulty in DIFFICULTY_LEVELS else 1,
                      format_func=lambda d: d.split(" ")[0],
                      label_visibility="collapsed")
    st.session_state.difficulty = sd
    st.markdown('<hr class="r-div"/>', unsafe_allow_html=True)

    st.markdown('<div class="r-head">⚡ QUICK ACTIONS</div>', unsafe_allow_html=True)
    if st.button("🧩 Start a Quiz", use_container_width=True, type="primary"):
        st.session_state.mode = "Quiz Mode"; st.session_state.active_nav = "Quiz Mode"
        qm.start_new_quiz(eff_subj, st.session_state.topic, st.session_state.difficulty)
        st.session_state.total_quizzes += 1
        with st.spinner(): qm.fetch_next_question(gemini_mgr)
        st.rerun()
    if st.button("💡 Explain Mode", use_container_width=True):
        st.session_state.mode = "Explain Mode"; st.session_state.active_nav = "Chat"; st.rerun()
    if st.button("📝 Exam Mode", use_container_width=True):
        st.session_state.mode = "Exam Mode"; st.session_state.active_nav = "Chat"; st.rerun()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []; st.toast("Chat cleared!", icon="🧹"); st.rerun()
    st.markdown('<hr class="r-div"/>', unsafe_allow_html=True)

    if st.session_state.recent_topics:
        st.markdown('<div class="r-head">🕒 RECENT TOPICS</div>', unsafe_allow_html=True)
        for t in st.session_state.recent_topics[:5]:
            st.markdown(f"""
            <div class="topic-pill">
                <div><div class="tp-name">{t['name']}</div><div class="tp-cnt">{t['count']} msg(s)</div></div>
                <div class="tp-arr">›</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('<hr class="r-div"/>', unsafe_allow_html=True)

    st.markdown('<div class="r-sdg-note">🌱 Supporting SDG 4 — Quality Education for All 🌍</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
