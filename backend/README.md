# API Documentation Generator - Backend

FastAPI backend for extracting API endpoints from GitHub repositories.

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running

**From the backend directory:**

```bash
python main.py
```

Or use the startup script:
- **Windows**: `run.bat`
- **Linux/Mac**: `bash run.sh`

Server runs at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Environment Variables

Create `.env` file in the backend directory:

```
GITHUB_TOKEN=github_pat_your_token
FRONTEND_URL=http://localhost:3000
```

## Project Structure

```
api_doc_generator/
├── github/              # GitHub API integration
├── scanner/             # Repository scanning & file detection
├── extractors/          # Framework-specific extractors
├── models/              # Pydantic data models
├── routes/              # FastAPI routes
└── services/            # Utility services
```

## API Endpoints

- `POST /api/api-docs/scan-repository` - Scan repository for backend files
- `POST /api/api-docs/extract-endpoints` - Extract API endpoints
- `GET /health` - Health check

See main README for full documentation.
