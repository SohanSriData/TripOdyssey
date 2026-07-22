# Trip Odyssey

Trip Odyssey is an AI-powered travel planner with a FastAPI backend and Streamlit frontend. It generates travel itineraries, budgets, hotels, transport, attractions, and destination guidance using a chat model.

## Features

- FastAPI backend exposing a `/query` endpoint
- Streamlit UI for submitting travel requests
- AI-driven itinerary generation
- Saves generated plans to a document file
- Uses Groq or OpenAI as the model provider

## Requirements

- Python 3.10+
- `GROQ_API_KEY` in environment for Groq
- `OPENAI_API_KEY` in environment for OpenAI (optional)
- `GPLACES_API_KEY` for Google Places search
- `OPENWEATHERMAP_API_KEY` for weather lookups
- `EXCHANGE_RATE_API_KEY` for currency conversion
- `ALPHAVANTAGE_API_KEY` for currency exchange rates (arithmetic tool)

## Installation

1. Activate your virtual environment:

Windows:
```powershell
c:\Users\sohan\Projects\AI_Trip_Planner\env\Scripts\activate
```

Linux/macOS:
```bash
source env/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the backend

Start the FastAPI server:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## Running the frontend

In a separate terminal, start Streamlit:

```powershell
streamlit run streamlit_app.py
```

Then open the Streamlit app in your browser.

## Notes

- The Streamlit app posts requests to `http://localhost:8000/query`.
- If you use the OpenAI provider in code, set `OPENAI_API_KEY` as well.
- The backend loads model configuration from `config/config.yaml` and environment variables.
