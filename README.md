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

1. Create and activate a virtual environment:

Windows:
```powershell
python -m venv env
env\Scripts\activate
```

Linux/macOS:
```bash
python3 -m venv env
source env/bin/activate
```

2. Upgrade pip and install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your API keys:

```env
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
GPLACES_API_KEY=your_google_places_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
ALPHAVANTAGE_API_KEY=your_alphavantage_api_key
```

> Do not commit `.env` to GitHub. It should stay local to your machine.

## Running the backend

Start the FastAPI server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## Running the frontend

In a separate terminal with the virtual environment activated:

```bash
streamlit run streamlit_app.py
```

Then open the Streamlit app in your browser.

## Notes

- The Streamlit app posts requests to `http://localhost:8000/query`.
- `config/config.yaml` contains additional model configuration.
- Your local `.env` file is ignored by `.gitignore` and should not be uploaded.
