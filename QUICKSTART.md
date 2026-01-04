# Quick Start Guide

## Phase 1: Text-Only Theory Interview

This guide will help you get the AI Interview Platform running for Phase 1 (text-only theory interviews).

## Prerequisites

1. **Python 3.11+** installed
2. **Google Gemini API Key** - Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Setup Steps

### 1. Install Dependencies

```bash
pip install -e .
```

### 2. Configure Environment

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_api_key_here
DEBUG=true
```

### 3. Start the Server

```bash
# Option 1: Using uvicorn directly
uvicorn app.main:app --reload

# Option 2: Using Python module
python -m app.main
```

The API will be available at `http://localhost:8000`

### 4. Test the API

#### Using curl:

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Create an interview
curl -X POST http://localhost:8000/api/v1/interviews \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "Alice Smith",
    "theory_topic": "bias-variance tradeoff",
    "interview_type": "ml_junior"
  }'

# Submit a response (replace {interview_id} with actual ID)
curl -X POST http://localhost:8000/api/v1/interviews/{interview_id}/respond \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Overfitting occurs when a model learns the training data too well..."
  }'
```

#### Using the example script:

```bash
# Make sure server is running first
python example_usage.py
```

#### Using the interactive API docs:

Visit `http://localhost:8000/docs` for Swagger UI or `http://localhost:8000/redoc` for ReDoc.

## API Endpoints

### POST `/api/v1/interviews`
Create a new interview session.

**Request:**
```json
{
  "candidate_name": "John Doe",
  "theory_topic": "bias-variance tradeoff",
  "interview_type": "ml_junior"
}
```

**Response:**
```json
{
  "interview_id": "uuid",
  "candidate_id": "uuid",
  "message": "Interview created successfully",
  "interviewer_response": {
    "speech": "What does overfitting mean?",
    "meta": {
      "phase": 1,
      "followup_used": false,
      "flag_vague": false,
      "flag_incorrect": false,
      "end_theory_round": false
    }
  }
}
```

### GET `/api/v1/interviews/{interview_id}`
Get current interview state.

### POST `/api/v1/interviews/{interview_id}/respond`
Submit a candidate response and get the next question.

**Request:**
```json
{
  "message": "Your answer here..."
}
```

## Interview Flow

1. **Create Interview** → Get initial question
2. **Submit Response** → Get follow-up question
3. **Continue** → Interviewer adapts based on responses
4. **Complete** → Theory round ends after 3 phases

## Troubleshooting

### "GEMINI_API_KEY not found"
- Make sure `.env` file exists and contains `GEMINI_API_KEY=your_key`

### "Module not found" errors
- Run `pip install -e .` to install the package in editable mode

### API returns 500 errors
- Check server logs for detailed error messages
- Verify your Gemini API key is valid
- Ensure you have API quota available

## Next Steps

Once Phase 1 is working:
- Test with different theory topics
- Verify state management works correctly
- Prepare for Phase 2 (voice integration)

