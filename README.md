# EduGenie: Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational AI assistant based on the supplied project documentation. It provides:

- Q&A
- Beginner-friendly concept explanations
- Multiple-choice quiz generation
- Educational passage summarization
- Personalized learning paths

## Architecture

```text
EduGenie/
├── main.py
├── config.py
├── ai_service.py
├── schemas.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    └── test_app.py
```

## How the implementation maps to the supplied documentation

The document specifies FastAPI, HTML/CSS, Gemini for Q&A/summarization/quizzes/learning paths, and LaMini-Flan-T5-783M for concept explanation. Those modules are implemented as separate Python files and exposed through `/qa`, `/explain`, `/quiz`, `/summarize`, and `/learn/recommendations`.

The supplied document names Gemini 1.5 Pro. The code deliberately makes the Gemini model configurable through `GEMINI_MODEL` because Gemini model availability changes over time. The default is a current configurable model value rather than hard-coding the retired project-era model name.

## Requirements

- Windows/macOS/Linux
- Python 3.10+
- VS Code
- Internet connection for Gemini API calls
- A Gemini API key for Q&A, quiz, summary and learning path
- Internet connection for the first LaMini-Flan-T5 model download if using local explanation

## Windows + VS Code setup

Open the EduGenie folder in VS Code.

### 1. Create a virtual environment

PowerShell:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If `py` is unavailable:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The first installation of PyTorch/Transformers may take time.

### 3. Create the environment file

Copy:

```text
.env.example
```

to:

```text
.env
```

Then open `.env` and replace:

```text
GEMINI_API_KEY=PASTE_YOUR_GEMINI_API_KEY_HERE
```

with your own key.

Never publish `.env` or your API key.

### 4. Start the server

```powershell
uvicorn main:app --reload
```

You should see a local address such as:

```text
http://127.0.0.1:8000
```

Open that address in Chrome/Edge.

## Testing

### Browser test

1. Open the home page.
2. Select Q&A.
3. Ask: `Which is the largest ocean?`
4. Click Get Answer.
5. Test Explain with `Photosynthesis`.
6. Test Quiz with `Pythagoras theorem`.
7. Paste a paragraph into Summary.
8. Test Learning Path with `SQL`, Beginner, and a learning goal.

### API health test

Open:

```text
http://127.0.0.1:8000/health
```

Expected:

```json
{"status":"ok","service":"EduGenie"}
```

### Automated tests

With the virtual environment active:

```powershell
pytest
```

The included tests do not call Gemini. They check the application shell, health endpoint and request validation.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web interface |
| GET | `/health` | Health check |
| POST | `/qa` | Question answering |
| POST | `/explain` | Concept explanation |
| POST | `/quiz` | Quiz generation |
| POST | `/summarize` | Text summarization |
| POST | `/learn/recommendations` | Learning path |

FastAPI also provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

## Explanation model note

The supplied project document specifies `LaMini-Flan-T5-783M` for local concept explanations. This project keeps that design. The model is loaded lazily, only when Explain is first used.

The first Explain request can therefore take longer because the model must be downloaded and loaded. If local inference is not suitable for the computer, set:

```text
EXPLANATION_BACKEND=gemini
```

and restart the server.

## Troubleshooting

### `GEMINI_API_KEY is not configured`

Make sure the file is named exactly `.env` and contains a valid key.

### Gemini model error

Change `GEMINI_MODEL` in `.env` to a model currently available to your API account.

### Local explanation is slow

This is expected on CPU. The local LaMini model is hundreds of millions of parameters and is intended as the documentation's local explanation model. Use `EXPLANATION_BACKEND=gemini` if needed.

### PowerShell blocks activation

You can use Command Prompt instead:

```cmd
.venv\Scripts\activate.bat
```

or run commands through the VS Code terminal after selecting the Python interpreter from `.venv`.

## Security

- Keep API keys only in `.env`.
- `.env` is excluded by `.gitignore`.
- Do not paste API keys into source code or commit them to GitHub.
- For a public deployment, add authentication, rate limiting, logging controls and secret management.

## Project flow

```text
Browser
   |
   | POST JSON
   v
FastAPI (main.py)
   |
   +--> qna.py --------------------> Gemini
   |
   +--> quiz_module.py ------------> Gemini structured JSON
   |
   +--> summary_module.py ---------> Gemini
   |
   +--> learning_path.py ----------> Gemini structured JSON
   |
   +--> explanation_module.py -----> LaMini local
                          |
                          +--------> Gemini fallback (optional)
```
