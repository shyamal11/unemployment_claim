from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import streamlit.web.bootstrap as bootstrap
import sys
import os
import threading
import time
import subprocess
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Streamlit in a separate process
    streamlit_process = subprocess.Popen([
        "streamlit", "run",
        "frontend/app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true"
    ])
    yield
    # Cleanup
    streamlit_process.terminate()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Streamlit app is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 