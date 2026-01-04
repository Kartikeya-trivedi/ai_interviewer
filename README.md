<<<<<<< HEAD
# ai_interviewer
=======
# AI Interview Platform

Production-grade AI interview platform with voice interaction and code execution capabilities.

## Architecture

**Core Principle: Separation of Concerns**
- **Interviewer Agent**: Voice-facing, conducts the interview (theory + coding)
- **Judge Agent**: Silent evaluator, provides final assessment
- **State Management**: External state tracking (not LLM-managed)

## Phase 1: Text-Only Theory Interview (Current)

This phase implements:
- FastAPI backend with async support
- Google Gemini API integration (gemini-1.5-flash for interviewer)
- Interview state management (in-memory)
- 3-phase theory interview flow
- RESTful API endpoints

### Features

- **Create Interview**: Start a new interview session
- **Submit Response**: Candidate responds, interviewer asks follow-up
- **State Tracking**: External state management for flow control
- **Adaptive Follow-ups**: Interviewer adapts based on candidate responses

## Setup

### Prerequisites

- Python 3.11+
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd ai-interview-platform
```

2. Install dependencies:
```bash
pip install -e .
```

3. Create `.env` file:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

4. Run the application:
```bash
python -m app.main
# Or
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /api/v1/health
```

### Create Interview
```
POST /api/v1/interviews
{
  "candidate_name": "John Doe",
  "theory_topic": "bias-variance tradeoff",
  "interview_type": "ml_junior"
}
```

### Get Interview State
```
GET /api/v1/interviews/{interview_id}
```

### Submit Response
```
POST /api/v1/interviews/{interview_id}/respond
{
  "message": "Overfitting occurs when a model learns the training data too well..."
}
```

## Project Structure

```
/app
├── main.py                 # FastAPI entry point
├── config.py               # Pydantic settings
├── /api/v1                 # API endpoints
├── /agents                 # AI agents (interviewer, judge)
├── /services               # External service integrations
├── /core                   # State management, prompts
└── /models                 # Pydantic schemas
```

## Development Roadmap

### Phase 1 (Current) ✅
- [x] FastAPI skeleton
- [x] Gemini integration
- [x] State management
- [x] Theory interview flow

### Phase 2 (Next)
- [ ] LiveKit integration
- [ ] STT (Deepgram/Whisper)
- [ ] TTS (ElevenLabs)
- [ ] Voice interview

### Phase 3
- [ ] Docker sandbox
- [ ] Code execution
- [ ] Coding interview

### Phase 4
- [ ] Judge agent
- [ ] Async evaluation queue
- [ ] Final report generation

### Phase 5
- [ ] PostgreSQL + Redis
- [ ] Monitoring (Prometheus)
- [ ] Production hardening

## Testing

```bash
# Run tests (when implemented)
pytest
```

## License

MIT

>>>>>>> 3448365 (initial commit)
