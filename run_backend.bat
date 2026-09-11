@echo off
echo Starting StudyBuddy FastAPI Backend on http://localhost:8000 ...
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
pause
