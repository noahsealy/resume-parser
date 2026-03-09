# Resume Parser

Recording Highlighting Project: https://www.loom.com/share/5a043625fca24603a014cadd9d9a5d92

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
tests/            # Unit test suite
main.py           # Entry point
pytest.ini        # Pytest configuration
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

Update the file paths in `main.py` to point to your resumes, then run:

```bash
python main.py
```

`main.py` demonstrates both supported formats:

```python
# Example 1: Parse a PDF resume
pdf_result = framework.parse_resume('NoahSealyResume.pdf')

# Example 2: Parse a Word resume
docx_result = framework.parse_resume('NoahSealyResume.docx')
```

Each call returns a `ResumeData` object serialized as JSON:

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "skills": ["Python", "SQL", "Docker"]
}
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

## Running Tests

The test suite uses `pytest` and `unittest.mock` — no API key or network access required.

```bash
pytest
```

To run with verbose output:

```bash
pytest -v
```

To run an individual test file:

```bash
pytest tests/test_foo.py
```

To run a single test by name:

```bash
pytest tests/test_foo.py::test_function_name
```

### Test Coverage

| File                             | What's tested                                                            |
| -------------------------------- | ------------------------------------------------------------------------ |
| `tests/test_email_extractor.py`  | Regex matching, multiple emails, type validation                         |
| `tests/test_name_extractor.py`   | Happy path, whitespace trimming, retry logic, sleep behavior             |
| `tests/test_skills_extractor.py` | JSON parsing, code fence stripping, retry logic, invalid response errors |
| `tests/test_prompts.py`          | Prompt string output, required keywords for TestClient matching          |
| `tests/test_parsers.py`          | PDF/Word parsing via mocked readers, empty file handling                 |
| `tests/test_resume_extractor.py` | Full extraction pipeline with TestClient, missing extractor defaults     |
| `tests/test_framework.py`        | File routing, unsupported extension error, end-to-end pipeline           |
| `tests/test_resume_data.py`      | JSON serialization, field correctness, edge cases (None, empty skills)   |

All LLM calls are handled by `TestClient` or `unittest.mock` — the suite runs fully offline.
