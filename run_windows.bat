@echo off
if not exist .venv (
  py -3.10 -m venv .venv 
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
if not exist .env copy .env.example .env
echo.
echo EduGenie is ready.
echo Add your GEMINI_API_KEY to .env, then run:
echo uvicorn main:app --reload
pause
