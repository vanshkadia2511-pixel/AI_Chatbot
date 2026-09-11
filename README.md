# StudyBuddy 📚 — AI Learning Tutor for SDG 4

> **SDG 4 — Quality Education** | Next Gen Chatbot Arena Submission
> Built with Python · Streamlit · Google Gemini

---

## 🎯 What is StudyBuddy?

**StudyBuddy** is a competition-ready AI learning tutor purpose-built for **SDG 4 — Quality Education**.

It helps students:

- understand academic concepts at their level
- practice with interactive quizzes
- revise efficiently for exams
- receive honest, structured, adaptive feedback

StudyBuddy is **not** a generic chatbot. It is a focused educational companion that adapts to learner level, follows multi-step instructions, and redirects off-topic conversations toward learning.

---

## 🏆 Competition Scoring Alignment

| Criterion | Weight | How StudyBuddy addresses it |
|---|---:|---|
| SDG Relevance & Problem Fit | 20 | Hard-coded educational focus; politely redirects off-topic requests |
| Response Quality & Helpfulness | 20 | Strong system prompt; structured, example-driven answers |
| Accuracy & Reliability | 20 | Honest uncertainty handling; never fabricates facts or citations |
| Functionality & Technical Quality | 15 | 4 learning modes, quiz engine, API endpoint, model fallback |
| Safety & Responsible AI | 10 | Content guardrails; no secret exposure; friendly error messages |
| Conversation & UX | 10 | Full session memory; clean sidebar; mobile-friendly layout |
| Innovation | 5 | Adaptive Learning Loop — explanation depth adjusts dynamically |
| **TOTAL** | **100** | |

---

## ✨ Features

| Mode | Icon | What it does |
|---|---|---|
| **Study Mode** | 📚 | Step-by-step tutoring with real-world examples and quick understanding checks |
| **Quiz Mode** | 🧩 | Interactive MCQ — 1 question at a time, instant feedback, score tracking |
| **Exam Mode** | 📝 | High-yield revision: definitions, formulas, common pitfalls, model answers |
| **Explain Mode** | 💡 | 3-level breakdown: Simple Analogy → College Standard → Advanced Deep Dive |

Additional capabilities:

- 🧠 **Session memory** — full conversation history sent to Gemini on every turn
- 📊 **Adaptive difficulty** — responses scale with selected learner level (Beginner → Advanced)
- 🔒 **Secret protection** — `.env`, Streamlit Secrets, `.gitignore` enforced
- ⚠️ **Friendly error handling** — wrong key, rate limits, missing config — no crashes, no exposed credentials
- 🎯 **SDG 4 guardrail** — politely redirects non-educational requests toward learning

---

## 🏗️ Architecture

```text
                         ┌────────────────────┐
                         │       USER         │
                         └─────────┬──────────┘
                                   │
                      ┌────────────┴────────────┐
                      ↓                         ↓
              WEB CHAT UI                EXTERNAL API
              Streamlit                  POST /chat
              (app.py)                  (api.py)
                      │                         │
                      └────────────┬────────────┘
                                   ↓
                         ┌────────────────────┐
                         │   STUDYBUDDY CORE  │
                         │                    │
                         │  system prompt     │
                         │  learner level     │
                         │  conversation      │
                         │  mode / subject    │
                         │  response policy   │
                         └─────────┬──────────┘
                                   ↓
                         ┌────────────────────┐
                         │   GEMINI API       │
                         │  (gemini_client)   │
                         └─────────┬──────────┘
                                   ↓
                         response validation
                                   ↓
                         WEB / API response
```

> The web UI and external API share the **same core chatbot logic**. No duplicate implementations.

---

## 📁 Project Structure

```text
AI_Chatbot/
│
├── app.py               # Streamlit web UI — chat orchestration, mode routing
├── api.py               # FastAPI REST endpoint — POST /chat
├── config.py            # Constants: models, subjects, difficulty, secrets loader
├── prompts.py           # System prompt builder and mode-specific modifiers
├── gemini_client.py     # Google GenAI SDK wrapper with error handling + fallback
├── quiz_manager.py      # MCQ quiz generator, score tracker, session state
│
├── requirements.txt     # Python dependencies
├── .env                 # Your local API key (never committed)
├── .env.example         # Safe template — commit this
├── .gitignore           # Excludes .env, .venv/, __pycache__/
│
├── .streamlit/
│   └── config.toml      # Streamlit theme and layout config
│
└── README.md            # This file
```

---

## 🔌 External API

StudyBuddy exposes a first-class REST API endpoint for machine evaluation and external integration.

### Endpoint

```http
POST /chat
Content-Type: application/json
```

### Request

```json
{
  "message": "Teach me the basics of linear regression."
}
```

### Success Response

```json
{
  "response": "Linear regression is a method to find the best-fit straight line..."
}
```

### Validation Error

```json
{
  "error": "Invalid request."
}
```

### Server / AI Failure

```json
{
  "error": "Unable to generate a response right now."
}
```

The API uses the identical StudyBuddy core (same system prompt, same Gemini integration) as the web UI.

---

## 🧠 System Prompt Strategy

StudyBuddy uses a structured four-section system prompt:

```text
ROLE    → StudyBuddy, AI learning tutor for SDG 4
TASK    → Explain · Practice · Revise · Feedback
CONTEXT → Learner level + subject + topic + mode
RULES   → 17 behavioral rules covering accuracy, honesty, safety, adaptation
```

Key behavioral rules enforced:

1. Stay focused on education and learning
2. Adapt explanations to learner level
3. Follow multi-step instructions completely
4. Provide examples when useful
5. Give practice questions when requested
6. Admit uncertainty honestly — never fabricate facts, citations, or statistics
7. Redirect off-topic requests politely toward learning
8. Never attempt to detect or exploit evaluation prompts

---

## 📊 Learner Levels

| Level | What changes in the response |
|---|---|
| Beginner | Intuitive analogies, everyday language, no jargon |
| Intermediate | Formal definitions, standard curriculum depth |
| Advanced | Technical reasoning, edge cases, deeper theory |
| Exam-Focused | High-yield revision, formulas, model exam answers |

Level selection genuinely changes the generated response — it is not just a UI label.

---

## 🧩 Quiz Mode Flow

```text
Topic selected
      ↓
Question generated by Gemini (MCQ format)
      ↓
Student selects option A / B / C / D
      ↓
Immediate evaluation (correct / incorrect)
      ↓
Explanation + optional hint shown
      ↓
Score updated
      ↓
Next question generated
      ↓
Final score on completion
```

Each question includes:

- Clear question statement
- Four labeled options (A, B, C, D)
- Correct answer evaluation
- Explanation of why the answer is correct (and why others are wrong)
- Hint for stuck students

---

## 🔄 Adaptive Learning Loop

StudyBuddy's core innovation:

```text
Explain concept at selected level
        ↓
Check understanding (quick question)
        ↓
Detect difficulty from learner response
        ↓
Adapt explanation depth accordingly
        ↓
Generate practice at appropriate difficulty
        ↓
Give structured feedback
        ↓
Increase or decrease difficulty
```

This adaptive loop makes StudyBuddy genuinely useful rather than a simple question-answering machine.

---

## 🛠️ Module Reference

### `config.py`

Centralises all application constants:

```python
DEFAULT_MODEL  = "gemini-3.6-flash"
FALLBACK_MODEL = "gemini-flash-latest"

LEARNING_MODES = { "Study Mode", "Quiz Mode", "Exam Mode", "Explain Mode" }

PREDEFINED_SUBJECTS = [
    "Computer Science & Programming",
    "Mathematics & Statistics",
    "Physics", "Chemistry",
    "Electrical & Electronics Engineering",
    "Mechanical & Civil Engineering",
    "Business, Finance & Economics",
    "Biology & Biotechnology",
    "General Studies & Humanities",
    "Other (Specify Below)",   # supports custom subjects
]

DIFFICULTY_LEVELS = [
    "Beginner (Foundational concepts)",
    "Intermediate (Standard college curriculum)",
    "Advanced (Deep analytical / theoretical)",
    "Exam-Focused (High-yield practice & formulas)",
]
```

### `prompts.py`

Builds the system instruction dynamically per session:

```text
BASE_SYSTEM_PROMPT
      +
SESSION CONTEXT (mode + subject + topic + level)
      +
MODE MODIFIER (Study / Quiz / Exam / Explain)
```

### `gemini_client.py`

All Gemini API calls with automatic error handling:

```text
Send conversation history
        ↓
Gemini API (primary model)
        ↓
Return response text
        ↓
On failure → attempt FALLBACK_MODEL
        ↓
Catch: 401/403 invalid key
        429 rate limit / quota exceeded
        network failure
        ↓
Show friendly message — never crash — never expose credentials
```

### `quiz_manager.py`

Interactive MCQ engine backed by Gemini:

```text
Generate question via Gemini (structured JSON output)
        ↓
Parse and validate JSON
        ↓
Display A/B/C/D choices
        ↓
User selects answer
        ↓
Immediate feedback + explanation
        ↓
Track score and history
        ↓
Generate next question
```

### `api.py`

Lightweight FastAPI REST layer:

```text
POST /chat  (JSON body: { "message": "..." })
        ↓
Validate input
        ↓
Call StudyBuddy core (same as web UI)
        ↓
Return { "response": "..." }
        ↓
On error: { "error": "..." } with appropriate HTTP status
```

---

## ⚠️ Error Handling

| Error condition | User sees | Behaviour |
|---|---|---|
| Missing API key | "Please enter your Gemini API key" | Sidebar prompt shown |
| Invalid API key | "Invalid API Key — verify at AI Studio" | Friendly message, no crash |
| Rate limit (429) | "Rate limit reached — please wait" | Friendly message, no crash |
| Network failure | "Unable to reach Gemini API" | Fallback model attempted |
| Empty / missing input | "Invalid request" | 400 response from API |
| Model failure | "Could not generate a response" | Fallback model tried |

**No stack traces, API keys, or internal credentials are ever shown to users.**

---

## 🔒 Secret Management

| Environment | Where the key lives |
|---|---|
| Local development | `.env` file (excluded from git via `.gitignore`) |
| Production (Streamlit Cloud) | Streamlit Secrets (platform-level) |
| Sidebar override | Runtime input (not stored permanently) |

Key lookup priority in `config.py`:

```text
1. Sidebar runtime input
        ↓
2. .env file (local development)
        ↓
3. Streamlit Cloud Secrets (production)
```

`.gitignore` excludes:

```text
.env
.venv/
__pycache__/
```

> **Never put your API key in Python source code or commit it to GitHub.**

---

# 1. Before You Start

You need:

| Requirement | Purpose |
|---|---|
| Python 3.10+ | Run the application |
| Git | Version control and deployment |
| VS Code / Antigravity / Cursor | Edit and build |
| Google account | Get a Gemini API key |
| GitHub account | Deploy the project |

Check your installations:

### Python

```bash
python3 --version
```

On Windows:

```bash
python --version
```

### Git

```bash
git --version
```

> On Windows, install Python with **"Add to PATH"** enabled.

---

# 2. Clone the Project

```bash
git clone https://github.com/YOUR-USERNAME/AI_Chatbot.git
cd AI_Chatbot
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Activate it

**Mac / Linux**

```bash
source .venv/bin/activate
```

**Windows PowerShell / CMD**

```bash
.venv\Scripts\activate
```

When activated, you see `(.venv)` at the start of your terminal line.

---

# 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

**Dependencies:**

```text
streamlit>=1.35.0
google-genai>=1.0.0
python-dotenv>=1.0.0
```

### What each library does

- `streamlit` — creates the chat UI and sidebar controls
- `google-genai` — communicates with the Gemini API
- `python-dotenv` — reads the API key safely from `.env`

---

# 4. Set Up the Gemini API Key

Get your API key from [Google AI Studio](https://aistudio.google.com/).

Copy the template:

```bash
cp .env.example .env
```

Open `.env` and add your key:

```env
GEMINI_API_KEY=paste-your-key-here
```

### Key lookup priority (handled by `config.py`)

```text
1. Sidebar input at runtime
       ↓
2. .env file (local development)
       ↓
3. .env.example fallback
       ↓
4. Streamlit Cloud Secrets (production)
```

**Important:** Never put the API key directly in Python code or commit it to GitHub.

---

# 5. Run StudyBuddy Locally

```bash
python -m streamlit run app.py
```

Your browser opens:

```text
http://localhost:8501
```

### Test the following

- Normal questions in **Study Mode**
- Follow-up questions (conversation memory)
- **Quiz Mode** — complete an MCQ round and check score
- **Exam Mode** — ask for high-yield revision points
- **Explain Mode** — ask for a concept explained at 3 levels
- Change subject and difficulty from the sidebar
- **Clear chat** button
- Missing API key behaviour

Stop the application with `Ctrl+C`.

---

# 6. Deploy to the Internet

## Step 1 — Initialize Git

```bash
git init
git add .
git status
```

### IMPORTANT

Check the output. `.env` **must NOT appear**.

If it appears, fix `.gitignore` before continuing.

```bash
git commit -m "StudyBuddy AI chatbot — SDG 4 submission"
```

---

# 7. Create the GitHub Repository

Create a new **public** GitHub repository named `AI_Chatbot`.

Then connect your local project:

```bash
git remote add origin https://github.com/YOUR-USERNAME/AI_Chatbot.git
git push -u origin main
```

Verify on GitHub that `.env` is **not** in the repository.

---

# 8. Deploy with Streamlit Community Cloud

1. Sign in with GitHub at [share.streamlit.io](https://share.streamlit.io/).
2. Click **Create app** → Deploy a public app from GitHub.
3. Select repository: `YOUR-USERNAME/AI_Chatbot`
4. Branch: `main`
5. Main file: `app.py`
6. Open **Advanced settings → Secrets** and add:

```toml
GEMINI_API_KEY = "paste-your-key-here"
```

7. Click **Deploy**.

You receive a public Streamlit URL:

```text
https://your-username-ai-chatbot-app-xxxx.streamlit.app
```

---

# 9. Understand Local `.env` vs Cloud Secrets

### On your laptop

```text
.env → GEMINI_API_KEY → Python application
```

### On Streamlit Cloud

```text
Streamlit Secrets → GEMINI_API_KEY → Python application
```

The key must:

- never be placed directly in code
- never be committed to GitHub
- never be publicly shared

---

# 10. Testing

### Representative test prompts

| Test | Prompt | Expected |
|---|---|---|
| Basic learning | `Explain photosynthesis to a beginner.` | Clear, simple explanation |
| SDG 4 example | `Teach me linear regression as a beginner, then give me 3 practice questions.` | Explanation + 3 questions |
| Follow-up | `Can you explain the second part again?` | Context retained |
| Level adaptation | `Explain this at an advanced level.` | Deeper, technical response |
| Quiz | `Quiz me on linear regression.` | Interactive MCQ starts |
| Ambiguous request | Vague question | Asks clarifying question |
| Off-topic | Non-educational request | Politely redirects |
| API endpoint | `POST /chat` with `{ "message": "Explain Newton's laws to a beginner." }` | Valid JSON response |
| Malformed API | `POST /chat` with `{}` or missing `message` | `{ "error": "Invalid request." }` |

### Competition Test Matrix

| Test | Expected |
|---|---|
| UI opens | PASS |
| Chat works | PASS |
| AI response appears | PASS |
| Context retained across turns | PASS |
| Beginner explanation works | PASS |
| Advanced explanation works | PASS |
| Quiz works | PASS |
| Score tracking works | PASS |
| Multi-part request works | PASS |
| Off-topic redirection works | PASS |
| Uncertainty handling works | PASS |
| API `POST /chat` works | PASS |
| Malformed API request handled | PASS |
| Missing key handled | PASS |
| API failure handled | PASS |
| No secret exposed | PASS |
| Public deployment works | PASS |

---

# 11. Troubleshooting

## Error: `No API key found`

`.env` file is missing or empty.

```env
GEMINI_API_KEY=your-key-here
```

File must be named exactly `.env` (with the dot prefix).

---

## Error: Gemini rejected the API key (401 / 403)

- Typo in the key
- Key generated for a different project
- Incorrect Streamlit Secret format

Fix: copy the key again from [Google AI Studio](https://aistudio.google.com/).
For Streamlit Secrets use: `GEMINI_API_KEY = "your-key"` (with quotes).

---

## Error: `429` / Too Many Requests

You have reached the free request quota. Wait and retry.
If persistent, create a new key in a separate AI Studio project.

---

## Error: `ModuleNotFoundError`

Virtual environment is not active.

```bash
# Mac / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

Then re-run the install and start commands.

---

## Error: `streamlit: command not found`

```bash
python -m streamlit run app.py
```

---

## Problem: Bot forgets previous messages

Full conversation history must be passed to Gemini on every turn.
Check `gemini_client.py` — `_convert_messages_to_sdk_contents` converts all prior messages.

---

## Problem: Quiz mode not working

Quiz state is stored in `st.session_state.quiz_state`.
Check `quiz_manager.py` — the session key must be consistent across reruns.

---

# 12. Quick Start Checklist

- [ ] Install Python 3.10+
- [ ] Install Git
- [ ] Clone the repository
- [ ] Create `.venv`
- [ ] Activate `.venv`
- [ ] `pip install -r requirements.txt`
- [ ] Get Gemini API key from Google AI Studio
- [ ] Create `.env` from `.env.example`
- [ ] Verify `.env` is in `.gitignore`
- [ ] `python -m streamlit run app.py`
- [ ] Test Study Mode
- [ ] Test Quiz Mode
- [ ] Test Exam Mode
- [ ] Test Explain Mode
- [ ] Test conversation memory (multi-turn)
- [ ] Test error handling (remove key temporarily)
- [ ] `uvicorn api:app --host 0.0.0.0 --port 8000`
- [ ] Test `POST /chat` via curl or Postman
- [ ] `git init` → `git add .` → `git status` (confirm no `.env`)
- [ ] Push to GitHub
- [ ] Deploy web app on Streamlit Community Cloud
- [ ] Add `GEMINI_API_KEY` to Streamlit Secrets
- [ ] Deploy API on Railway / Render / Fly.io
- [ ] Test public web URL
- [ ] Test public API URL
- [ ] Confirm repository has no exposed secrets

---

# Definition of Done

The project is complete only when:

- [ ] StudyBuddy runs as a web application
- [ ] Gemini / LLM integration works
- [ ] SDG 4 educational focus is strong
- [ ] System prompt is implemented
- [ ] Learner-level adaptation works
- [ ] Conversation context works
- [ ] Study Mode works
- [ ] Quiz Mode works
- [ ] Multi-step instructions work
- [ ] API endpoint exists (`api.py`)
- [ ] `POST /chat` works
- [ ] API returns documented JSON
- [ ] API handles errors
- [ ] UI handles errors
- [ ] Secrets are protected
- [ ] No credentials exposed client-side
- [ ] Representative prompts tested
- [ ] Public URL works
- [ ] Public API endpoint works
- [ ] Repository is clean
- [ ] README documentation exists
- [ ] Final version is stable
- [ ] No critical known bug remains

---

# 13. Make It Your Own

The personality of StudyBuddy is controlled entirely by `SYSTEM_PROMPT` in `prompts.py`:

```text
Role → Task → Context → Rules
```

Changing these sections transforms the same codebase into a completely different product:

```text
StudyBuddy  →  Fitness Coach
StudyBuddy  →  Cooking Helper
StudyBuddy  →  College Fest Support Bot
```

> **Same code + different prompt = different product.**

---

# 14. Core Concept

```text
User
 ↓
Streamlit UI         (app.py)
 ↓
Mode + Subject + Level   (config.py)
 ↓
System prompt builder    (prompts.py)
 ↓
Conversation history + system prompt
 ↓
Gemini API           (gemini_client.py)
 ↓
AI response
 ↓
Quiz engine if Quiz Mode (quiz_manager.py)
 ↓
Streamlit UI
```

> A small, well-engineered stack with a strong system prompt is more powerful than a large, unstable platform.

---

## 🔌 Running the API Server

In a separate terminal (while the Streamlit app runs on port 8501):

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

Test with curl:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain Newton's laws to a beginner."}'
```

API docs available at: `http://localhost:8000/docs`

### API Deployment Options

| Platform | Command / Notes |
|---|---|
| Railway | Free tier, set `GEMINI_API_KEY` env var, start command: `uvicorn api:app --host 0.0.0.0 --port $PORT` |
| Render | Free tier, same start command |
| Fly.io | Docker-friendly, good free tier |

Set `GEMINI_API_KEY` as an environment variable on your chosen platform.

---

## 🔗 Links

| Resource | URL |
|---|---|
| Google AI Studio (API key) | https://aistudio.google.com/ |
| Streamlit Cloud (web deploy) | https://share.streamlit.io/ |
| Railway (API deploy) | https://railway.app/ |
| Render (API deploy) | https://render.com/ |

---

*StudyBuddy — Built for SDG 4: Quality Education. Powered by Google Gemini.*
#   A I _ C h a t b o t  
 #   A I _ C h a t b o t  
 