# Resume Parser

A Python framework for extracting structured data from resumes. Given a PDF or Word document, it extracts the candidate's name, email address, and skills using a combination of regex-based parsing and LLM inference (Google Gemini).

## What It Does

- Parses `.pdf` and `.docx` resume files
- Extracts:
  - **Name** — via Gemini LLM
  - **Email** — via regex
  - **Skills** — via Gemini LLM (returns a JSON list)
- Returns a structured `ResumeData` object with all fields

## Project Structure

```
src/
  parsers/        # File parsers (PDF, Word)
  extractors/     # Field extractors (name, email, skills)
  prompts/        # LLM prompt templates
  inference/      # LLM client abstraction (Gemini + TestClient)
  framework/      # Orchestration (ResumeExtractor, ResumeParserFramework)
  models/         # ResumeData dataclass
main.py           # Entry point
```

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your values:
   ```bash
   cp .env.example .env
   ```

## Environment Variables

| Variable         | Description                                                                          |
| ---------------- | ------------------------------------------------------------------------------------ |
| `GEMINI_API_KEY` | Your Google Gemini API key (required in production)                                  |
| `APP_ENV`        | Set to `production` to use Gemini; omit or use any other value to use the TestClient |

## Usage

Update the file path in `main.py` to point to your resume, then run:

```bash
python main.py
```

The output is a `ResumeData` object:

```python
ResumeData(name='Jane Doe', email='jane@example.com', skills=['Python', 'SQL', 'Docker'])
```

## Test Client

When `APP_ENV` is not set to `production`, the app uses `TestClient` instead of Gemini. This allows local development and testing without an API key or network calls.

`TestClient` returns hardcoded responses based on prompt content:

| Prompt contains                                     | Returns        |
| --------------------------------------------------- | -------------- |
| `"extract all relevant technical and soft skills."` | `'["python"]'` |
| `"extract the full name of the candidate"`          | `'Noah Sealy'` |

To add new fake responses for additional extractors, add a matching `if` branch in `src/inference/test_client.py`:

```python
def generate(self, prompt: str) -> TestResponse:
    if 'your prompt keyword' in prompt:
        return TestResponse('your fake response')
    ...
```

To run in test mode (default when `APP_ENV` is unset):

```bash
# .env
APP_ENV=

python main.py
```

To run against real Gemini:

```bash
# .env
GEMINI_API_KEY=your_key_here
APP_ENV=production

python main.py
```
