# Unemployment Claims Assistant

An AI-powered application that helps users file and manage unemployment claims.

## Features

- Natural language interface for claim submission
- AI-powered fraud detection
- Eligibility rule checking
- User-friendly explanations of decisions

## Deployment Instructions

### Option 1: Streamlit Community Cloud (Recommended)

1. Create a GitHub repository and push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and main file (frontend/app.py)
6. Add your environment variables:
   - TOGETHER_API_KEY
   - DATABASE_URL (if using a database)

### Option 2: Docker Deployment

1. Build the Docker image:
```bash
docker build -t unemployment-claims .
```

2. Run the container:
```bash
docker run -p 8501:8501 -e TOGETHER_API_KEY=your_key unemployment-claims
```

## Environment Variables

Create a `.env` file with the following variables:
```
TOGETHER_API_KEY=your_together_api_key
DATABASE_URL=your_database_url
```

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
cd frontend
streamlit run app.py
```

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

---

## Getting Started (For New Users)

### Prerequisites

1. **Python 3.11**
   - [Download for Mac/Windows](https://www.python.org/downloads/)
   - Mac (Homebrew): `brew install python@3.11`
   - Linux: `sudo apt-get install python3.11 python3.11-venv python3.11-dev`
2. **Git**
   - [Download and install](https://git-scm.com/downloads)
3. **(Optional) VS Code**
   - [Download VS Code](https://code.visualstudio.com/)
   - Install the "Python" extension in VS Code

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/shyamal11/unemployment_claim.git
   cd unemployment_claim
   ```
2. **Create a virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
   - Copy or create a `.env` file in the project root with:
     ```
     TOGETHER_API_KEY=your_api_key_here
     DATABASE_URL=your_database_url_here
     ```
5. **Initialize the database**
   ```bash
   python init_db.py
   ```
6. **Run the application**
   ```bash
   cd frontend
   streamlit run app.py
   ```
   - The app will open in your browser at [http://localhost:8501](http://localhost:8501)

### Summary Table

| Step | What to Install/Do         | Command/Link                                      |
|------|----------------------------|---------------------------------------------------|
| 1    | Python 3.11                | [python.org](https://www.python.org/downloads/)   |
| 2    | Git                        | [git-scm.com](https://git-scm.com/downloads)      |
| 3    | VS Code (optional)         | [VS Code](https://code.visualstudio.com/)         |
| 4    | Clone repo                 | `git clone ...`                                   |
| 5    | Virtual environment        | `python3.11 -m venv venv`                         |
| 6    | Install dependencies       | `pip install -r requirements.txt`                 |
| 7    | Set up .env file           | Edit `.env` in project root                       |
| 8    | Initialize database        | `python init_db.py`                               |
| 9    | Run the app                | `cd frontend && streamlit run app.py`             |

---

## Environment Variables

- `TOGETHER_API_KEY`: Your Together AI API key for embeddings and LLM
- `DATABASE_URL`: Your Postgres database connection string