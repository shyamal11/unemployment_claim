# Unemployment Claims Assistant

An AI-powered application that helps process and evaluate unemployment claims using fraud detection and eligibility checking.

## Features

- Natural language interface for claim submission
- AI-powered fraud detection
- Eligibility rule checking
- User-friendly explanations of decisions

## Deployment

This application is deployed on Streamlit Cloud. You can access it at: [Your Streamlit URL]

## Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`:
   ```
   TOGETHER_API_KEY=your_api_key_here
   ```
5. Initialize the database:
   ```bash
   python init_db.py
   ```
6. Run the application:
   ```bash
   streamlit run frontend/app.py
   ```

## Environment Variables

- `TOGETHER_API_KEY`: Your Together AI API key for embeddings and LLM

## Project Structure

```
├── frontend/
│   └── app.py              # Streamlit application
├── services/
│   ├── fraud_detector.py   # Fraud detection logic
│   ├── eligibility.py      # Eligibility checking
│   ├── embedding_service.py # Embedding generation
│   └── llm_service.py      # LLM integration
├── database/
│   ├── models.py           # Database models
│   └── __init__.py         # Database configuration
├── config.py               # Application configuration
├── init_db.py             # Database initialization
└── requirements.txt       # Project dependencies
```