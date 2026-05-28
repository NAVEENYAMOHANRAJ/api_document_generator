# Smart API Documentation Generator

Technology-independent API documentation generator for PS08. The app scans API source code, uploaded ZIP files, local folders, or existing OpenAPI/Swagger specs, then generates developer-friendly endpoint documentation.

## Is This Project AI-Based?

Yes. This project includes an optional AI/LLM enrichment layer.

The core endpoint extraction works without an OpenAI key by using deterministic parsers and framework-specific rules. When an OpenAI API key is added, the backend uses an LLM to improve endpoint summaries, descriptions, request notes, response notes, and error notes.

That means the project is still AI-powered by design:

- Without key: rule-based extraction and deterministic documentation.
- With key: rule-based extraction plus LLM-enhanced documentation.

For a zero-cost demo, keep LLM enrichment disabled:

```env
ENABLE_LLM_ENRICHMENT=false
OPENAI_API_KEY=
```

## Features

- Accepts GitHub repositories, local folders, and ZIP uploads.
- Detects API route files automatically.
- Extracts endpoint path and HTTP method.
- Extracts available request params, headers, body schema, response schema, and response codes.
- Supports existing OpenAPI/Swagger specs and merges them with code-discovered endpoints.
- Generates OpenAPI-like JSON, Markdown, and HTML documentation.
- Includes a web UI for previewing endpoints and exporting docs.
- Supports multiple backend stacks by design, including Laravel/PHP, FastAPI, Express, Flask, Django REST Framework, NestJS, Spring Boot, Go Gin/Fiber, and ASP.NET Core.

## Requirements

- Python 3.11+
- Node.js 18+
- npm

## Quick Start

The easiest way on Windows is:

```bat
start-demo.bat
```

This starts:

- Backend: `http://localhost:8001`
- Frontend: `http://localhost:3001`
- Backend Swagger docs: `http://localhost:8001/docs`

Open the app:

```text
http://localhost:3001
```

The frontend is connected to the backend through:

```env
NEXT_PUBLIC_API_URL=http://localhost:8001/api
```

## Manual Run Commands

### 1. Backend

```bat
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run_dev_server.py
```

Backend runs at:

```text
http://localhost:8001
```

Health check:

```text
http://localhost:8001/health
```

### 2. Frontend

Open a second terminal:

```bat
cd frontend
npm install
set NEXT_PUBLIC_API_URL=http://localhost:8001/api
npm run dev -- -p 3001
```

Frontend runs at:

```text
http://localhost:3001
```

## OpenAI API Key Setup

An OpenAI key is optional, but recommended if you want AI-enhanced endpoint descriptions.

Create an API key from the OpenAI Platform:

```text
https://platform.openai.com/api-keys
```

Official OpenAI docs explain that API keys should be kept secret and loaded from environment variables or a server-side key management system, not exposed in browser/client code.

### Add the key to the backend

Create this file:

```text
backend\.env
```

You can copy from:

```text
backend\.env.example
```

Then set:

```env
ENABLE_LLM_ENRICHMENT=false
OPENAI_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-4o-mini
LLM_API_URL=https://api.openai.com/v1/chat/completions
LLM_TIMEOUT_SECONDS=20
LLM_MAX_ENDPOINTS=40
```

For a paid/credit-enabled AI demo, change `ENABLE_LLM_ENRICHMENT` to `true`.

Restart the backend after changing `.env`.

## GitHub Token Setup

A GitHub token is optional. It is useful for private repositories and higher rate limits.

Create a GitHub token here:

```text
https://github.com/settings/tokens
```

Add it in `backend\.env`:

```env
GITHUB_TOKEN=your_github_pat_here
```

You can also paste a token in the UI when scanning a GitHub repository.

## Laravel/PHP Test Input

To test the included Laravel sample, choose **Local Path** in the UI and paste:

```text
C:\Users\NAVEENYA\OneDrive\Desktop\NAVEENYA\api_doc_generator\prototype_projects\multi_stack_api\laravel
```

Expected extracted endpoints:

```text
GET    /laravel-users
POST   /laravel-users
DELETE /laravel-users/{id}
```

## Run Tests

```bat
cd backend
venv\Scripts\activate
pytest
```

If you do not have `pytest` installed yet:

```bat
pip install -r requirements.txt
pytest
```

## Run Demo Matrix

This runs the 10-case verification matrix used for the PS08 demo:

```bat
python backend\tests\run_demo_matrix.py
```

Expected summary:

```text
Backend health endpoint: PASS
Frontend app: PASS
Swagger docs: PASS
Laravel local-folder extraction: PASS
ZIP upload extraction: PASS
Multi-stack extraction: PASS
OpenAPI spec extraction: PASS
Bad local path error handling: PASS
Bad ZIP error handling: PASS
Laravel edge cases: PASS
Zero-cost LLM fallback: PASS
```

## 10 Demo Test Links And Expected Output

1. `http://localhost:3001`
   - Output: frontend UI opens and uses `http://localhost:8001/api`.

2. `http://localhost:8001/health`
   - Output: `{"status":"ok"}`.

3. `http://localhost:8001/docs`
   - Output: FastAPI Swagger documentation page.

4. `http://localhost:8001/openapi.json`
   - Output: backend OpenAPI schema JSON.

5. `POST http://localhost:8001/api/api-docs/extract-local-folder`
   - Body: `{"folder_path":"C:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\prototype_projects\\multi_stack_api\\laravel"}`
   - Output: `GET /laravel-users`, `POST /laravel-users`, `DELETE /laravel-users/{id}`.

6. `POST http://localhost:8001/api/api-docs/extract-upload?filename=laravel.zip`
   - Body: ZIP file containing `routes/api.php`.
   - Output: same 3 Laravel endpoints.

7. `POST http://localhost:8001/api/api-docs/scan-repository`
   - Body: `{"repo_url":"owner/repo","github_token":null}`
   - Output: detected backend files and framework candidates when GitHub/network access is available.

8. `POST http://localhost:8001/api/api-docs/extract-endpoints`
   - Body: `{"repo_url":"owner/repo","github_token":null}`
   - Output: extracted endpoints, OpenAPI JSON, Markdown, and HTML when GitHub/network access is available.

9. `python backend\tests\run_demo_matrix.py`
   - Output: all matrix tests return `PASS`.

10. `npm.cmd run build` from `frontend`
   - Output: Next.js production build completes successfully.

## Build Frontend

```bat
cd frontend
npm run build
```

## Important Notes

- Do not put `OPENAI_API_KEY` in frontend code.
- Do not commit real `.env` files.
- The app works without an OpenAI key, but AI descriptions require one.
- Port `8000` may already be used by another app, so this project uses backend port `8001` in the demo script.

## Useful Links

- Frontend app: `http://localhost:3001`
- Backend API docs: `http://localhost:8001/docs`
- Backend health check: `http://localhost:8001/health`
- OpenAI API key page: `https://platform.openai.com/api-keys`
