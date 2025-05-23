# Unemployment Claims Application

A modern web application for processing unemployment insurance claims with AI-powered fraud detection and eligibility checking.

## Features

- Interactive chatbot interface for claim submission
- AI-powered fraud detection
- Automated eligibility checking
- Real-time claim status updates
- User-friendly dashboard

## Tech Stack

### Frontend
- React
- Material-UI
- TypeScript
- Axios for API calls

### Backend
- FastAPI
- Python
- SQLAlchemy
- OpenAI API for explanations
- Together API for LLM

## Local Development

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the backend directory with:
   ```
   OPENAI_API_KEY=your_openai_api_key
   SECRET_KEY=your_secret_key
   ```

4. Run the backend:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run the frontend:
   ```bash
   npm start
   ```

## Deployment

### Backend (Render)
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the build command: `pip install -r backend/requirements.txt`
4. Set the start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set the build command: `cd frontend && npm run build`
3. Set the output directory: `frontend/build`

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

MIT