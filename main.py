from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import router as api_router
import uvicorn
import subprocess
import threading
import os

app = FastAPI(title="Unemployment Fraud Detection API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

def run_streamlit():
    streamlit_port = int(os.getenv("PORT", "8000")) + 1
    subprocess.run([
        "streamlit", "run", "frontend/app.py",
        "--server.port", str(streamlit_port),
        "--server.address", "0.0.0.0"
    ])

if __name__ == "__main__":
    # Start Streamlit in a separate thread
    streamlit_thread = threading.Thread(target=run_streamlit)
    streamlit_thread.start()
    
    # Start FastAPI
    uvicorn.run(app, host="0.0.0.0", port=8000) 