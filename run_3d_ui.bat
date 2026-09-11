@echo off
echo Starting StudyBuddy 3D Frontend on http://localhost:5173 ...
python -m http.server 5173 --directory frontend
pause
