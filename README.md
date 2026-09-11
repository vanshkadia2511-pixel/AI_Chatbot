# StudyBuddy 📚 — Adaptive AI Learning Tutor for SDG 4

[![SDG 4 - Quality Education](https://img.shields.io/badge/SDG%204-Quality%20Education-C5192D?style=for-the-badge&logo=united-nations&logoColor=white)](https://sdgs.un.org/goals/goal4)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Three.js](https://img.shields.io/badge/Three.js-3D%20Interactive-black?style=for-the-badge&logo=three.js&logoColor=white)](https://threejs.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20%2F%202.0-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com/)

> **Next Gen Chatbot Arena Submission**  
> *Adaptive AI Tutor for Better Learning: Understand concepts, practice intelligently, and improve continuously.*

---

## 🎯 Executive Summary

**StudyBuddy** is a competition-ready AI learning companion purpose-built to advance **United Nations SDG 4 (Quality Education)**. Unlike standard chatbots that provide generic text answers, StudyBuddy functions as a **complete adaptive learning environment** that actively guides students through:

$$\text{Ask} \longrightarrow \text{Learn} \longrightarrow \text{Practice} \longrightarrow \text{Adapt} \longrightarrow \text{Improve}$$

The platform integrates a **3D intelligence layer**, multi-tier explanation depth, an interactive multiple-choice quiz engine, and automated difficulty scaling to ensure equitable, high-quality learning tailored to each student's pace.

---

## 🏆 Competition Scoring Alignment

| Criterion | Weight | How StudyBuddy Addresses It |
|---|:---:|---|
| **SDG 4 Relevance & Problem Fit** | **20%** | Hard-coded educational pedagogy; politely redirects non-learning prompts toward academic topics. |
| **Response Quality & Helpfulness** | **20%** | Structured educational responses (Analogy → Formulation → Examples → Quick Check). |
| **Accuracy & Reliability** | **20%** | Transparent uncertainty handling; zero hallucinated citations; grounded explanations. |
| **Functionality & Technical Depth** | **15%** | Dual interfaces (3D WebGL + Streamlit), FastAPI REST endpoint, model fallback logic. |
| **Safety & Responsible AI** | **10%** | Content guardrails, strict client-side secret protection, zero credential leakage. |
| **Conversation & UX** | **10%** | Multi-turn session memory, glassmorphism UI, mobile responsive drawers, Web Audio synthesis. |
| **Innovation & Differentiation** | **5%** | 3D visual intelligence layer (Knowledge Graph, Difficulty Wheel, Score Cube, Progress Helix). |

---

## 🏗️ System Architecture

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                              STUDENT / JUDGE                            │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
         ┌───────────────────────────┴───────────────────────────┐
         ▼                                                       ▼
┌─────────────────────────────────┐             ┌─────────────────────────────────┐
│   3D Interactive Web UI         │             │   Streamlit Web Interface       │
│   (frontend/index.html)         │             │   (app.py)                      │
│   Three.js · WebGL · HUD        │             │   Chat History · Sidebar        │
└────────────────┬────────────────┘             └────────────────┬────────────────┘
                 │                                               │
                 │  POST /chat (JSON)                            │ Direct Import
                 ▼                                               │
┌─────────────────────────────────┐                              │
│   FastAPI REST API Layer        │                              │
│   (api.py) — Port 8000          │                              │
└────────────────┬────────────────┘                              │
                 │                                               │
                 └───────────────────────┬───────────────────────┘
                                         ▼
                 ┌───────────────────────────────────────────────┐
                 │             STUDYBUDDY CORE ENGINE            │
                 │  • prompts.py       (System Prompt & Modes)   │
                 │  • config.py        (Subjects, Tiers, Models) │
                 │  • quiz_manager.py  (Pedagogical MCQ Engine)  │
                 │  • gemini_client.py (Google GenAI SDK)        │
                 └───────────────────────┬───────────────────────┘
                                         ▼
                 ┌───────────────────────────────────────────────┐
                 │             GOOGLE GEMINI API                 │
                 │   Primary: gemini-2.5-flash / gemini-1.5-flash│
                 │   Fallback: gemini-flash-latest               │
                 └───────────────────────────────────────────────┘
```

---

## ✨ Core Features & Learning Modes

### 1. The Four Learning Modes
| Mode | Icon | Pedagogical Focus |
|---|:---:|---|
| **Study Mode** | 📚 | Step-by-step tutoring with real-world intuition, formulas, and comprehension checks. |
| **Explain Mode** | 💡 | 3-tier progressive breakdown: *Simple Analogy* → *College Standard* → *Advanced Deep Dive*. |
| **Quiz Mode** | 🧩 | Interactive MCQ practice: immediate evaluation, detailed rationales, score & XP tracking. |
| **Exam Mode** | 📝 | High-yield revision: definitions, key formulas, common traps, and model exam answers. |

### 2. 3D Intelligence Visualizers
- 🪐 **Central Conversation Sphere**: Visualizes AI tutor status with 6 distinct states (`IDLE`, `THINKING`, `RESPONDING`, `SUCCESS`, `ERROR`, `QUIZ_EVALUATION`).
- 🛰️ **Orbiting Mode Satellites**: 3D interactive orbs that orbit the knowledge core and react to user selection.
- 🎯 **Segmented Difficulty Wheel**: 4-level ring indicating current cognitive depth (Beginner, Intermediate, Advanced, Exam-Focused).
- 🎲 **Holographic Score Cube**: Dynamically changes color based on accuracy (🔴 Low `<50%`, 🟡 Medium `50-79%`, 🟢 High `≥80%`).
- 🌐 **Interactive Knowledge Graph**: Connects prerequisite academic concepts with glowing links and click-to-learn navigation.
- 🧬 **Progress Helix**: Spiraling learning path tracking mastery from 0% to 100%.

---

## 📁 Repository Structure

```text
AI_Chatbot/
├── frontend/                     # 3D Three.js Interactive Learning Interface
│   ├── index.html                # Master application shell
│   ├── css/                      # Modular style system
│   │   ├── variables.css         # Design tokens, color palette & typography
│   │   ├── reset.css             # Base stylesheet
│   │   ├── layout.css            # Header, 3D workspace, sidebar & HUD grid
│   │   ├── components.css        # Glassmorphism cards, controls & badges
│   │   ├── chat.css              # AI message stream & quiz card styles
│   │   ├── 3d.css                # 3D canvas overlay & tooltips
│   │   ├── animations.css        # Glowing keyframes & floating XP toasts
│   │   └── responsive.css        # Mobile and tablet drawer layouts
│   └── js/                       # Modular ES6 JavaScript engine
│       ├── app.js                # Lifecycle coordinator & 30s Judge Demo Flow
│       ├── state.js              # Central reactive event hub & state store
│       ├── api.js                # Backend integration & offline fallback
│       ├── chat.js               # Chat controller & Markdown formatter
│       ├── quiz.js               # MCQ quiz bank & evaluation engine
│       ├── adaptive.js           # Real-time difficulty adaptation toasts
│       ├── animations.js         # Browser-native Web Audio synthesizer
│       ├── scene.js              # Three.js scene, lighting & raycaster
│       └── components/           # Modular 3D objects
│           ├── conversation-sphere.js
│           ├── mode-orbs.js
│           ├── difficulty-wheel.js
│           ├── score-cube.js
│           ├── knowledge-graph.js
│           ├── progress-helix.js
│           └── difficulty-indicator.js
│
├── api.py                        # FastAPI REST API (POST /chat, GET /health)
├── app.py                        # Streamlit web application
├── config.py                     # Constants, subject taxonomy & secret loader
├── prompts.py                    # Structured system prompt & mode modifiers
├── gemini_client.py              # Google GenAI SDK client with auto-fallback
├── quiz_manager.py               # Backend quiz state manager
│
├── run_backend.bat               # Windows launcher: FastAPI backend (Port 8000)
├── run_3d_ui.bat                 # Windows launcher: 3D Frontend (Port 5173)
├── run_streamlit.bat             # Windows launcher: Streamlit UI (Port 8501)
│
├── requirements.txt              # Production Python dependencies
├── .env.example                  # Environment template (Safe for git)
├── .gitignore                    # Protects secrets (.env) and caches
└── README.md                     # Master documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.10+** installed
- **Google Gemini API Key** (Obtain free at [Google AI Studio](https://aistudio.google.com/))

### 1. Installation & Setup
```bash
# Clone the repository
git clone https://github.com/vanshkadia2511-pixel/AI_Chatbot.git
cd AI_Chatbot

# Create and activate virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Secrets
Create a `.env` file from the template:
```bash
cp .env.example .env
```
Edit `.env` and paste your API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## ⚡ Running the Application

### Option A: One-Click Launchers (Windows)
Double-click the provided batch scripts in the project root:
1. `run_backend.bat` → Starts FastAPI backend on `http://localhost:8000`
2. `run_3d_ui.bat` → Starts 3D Three.js UI on `http://localhost:5173`
3. *(Optional)* `run_streamlit.bat` → Starts Streamlit chat on `http://localhost:8501`

### Option B: Terminal Execution

#### Terminal 1: Start FastAPI REST Backend
```powershell
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2: Start 3D Frontend Interface
```powershell
python -m http.server 5173 --directory frontend
```

#### Terminal 3: (Optional) Start Streamlit UI
```powershell
python -m streamlit run app.py
```

### Access URLs
- 🪐 **3D Interactive Learning UI**: [http://localhost:5173](http://localhost:5173)
- 📚 **Streamlit Web App**: [http://localhost:8501](http://localhost:8501)
- 🔌 **FastAPI Interactive Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ⏱️ 30-Second Judge Demonstration Flow

To experience the full capability of StudyBuddy in 30 seconds:

1. Open **[http://localhost:5173](http://localhost:5173)**.
2. Click the **`⚡ 30s Judge Demo`** button in the header bar.
3. Observe the automated evaluation loop:
   - **Step 1**: The system asks an introductory question at the **Beginner** level.
   - **Step 2**: The AI adapts visible depth, switching to **Advanced** with mathematical rigor.
   - **Step 3**: The interface transitions to **Quiz Mode**, evaluating MCQ answers and updating the **Score Cube** and **Progress Helix**.

---

## 🔌 REST API Specification

### Endpoint: `POST /chat`
Accepts learning prompts and returns structured educational feedback.

#### Request Payload
```json
{
  "message": "Teach me the basics of linear regression.",
  "subject": "Mathematics & Statistics",
  "level": "Intermediate",
  "mode": "Study Mode"
}
```

#### Successful Response (`200 OK`)
```json
{
  "response": "### Linear Regression 📈\nLinear regression models the relationship between a dependent variable..."
}
```

#### Health Check: `GET /` or `GET /health`
```json
{
  "status": "ok",
  "service": "StudyBuddy API",
  "version": "1.0.0",
  "sdg": "SDG 4 — Quality Education"
}
```

---

## 🔒 Security & Responsible AI

- **Zero Client-Side Exposure**: API keys are strictly accessed server-side via `config.py` and never injected into client JavaScript or HTML.
- **Git Protection**: `.gitignore` strictly excludes `.env`, preventing accidental token commits.
- **Content Safeguards**: Prompts enforce safety policies and academic guardrails, politely steering irrelevant or harmful requests back to educational topics.

---

## 🧪 Competition Test Matrix

| Scenario | Test Prompt / Action | Expected Result | Status |
|---|---|---|:---:|
| **Beginner Level** | `"Explain photosynthesis as a beginner"` | Simple analogies, intuitive everyday language | ✅ PASS |
| **Advanced Level** | `"Explain photosynthesis at an advanced level"` | Thylakoid membrane pathways, Calvin Cycle, RuBisCO | ✅ PASS |
| **Interactive Quiz** | `"Start a quiz on linear regression"` | MCQ format, option buttons, instant rationale | ✅ PASS |
| **Conversation Memory** | `"Can you elaborate on the second step?"` | Retains full previous context across multiple turns | ✅ PASS |
| **Off-Topic Guardrail** | `"Tell me celebrity gossip"` | Polite educational redirect to curriculum topics | ✅ PASS |
| **Offline Resilience** | Backend temporarily disconnected | Resilient educational fallback engine sustains demo | ✅ PASS |

---

## 🌐 Public Deployment Guide

### Deploy 3D UI (Vercel / Netlify / GitHub Pages)
- Set root directory to `frontend/`.
- Deploy as a static site without build commands.

### Deploy FastAPI Backend (Railway / Render)
- **Start Command**: `python -m uvicorn api:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**: `GEMINI_API_KEY=your_key`

### Deploy Streamlit App (Streamlit Community Cloud)
1. Link GitHub repository `AI_Chatbot` with main file `app.py`.
2. Add `GEMINI_API_KEY` under **App Settings → Secrets**.

---

## 📄 License & Attribution
Developed for the **Next Gen Chatbot Arena (SDG 4 Track)**.  
Built with ❤️ using Python, FastAPI, Three.js, and Google Gemini.