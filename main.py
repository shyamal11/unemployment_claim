import os
import sys
from pathlib import Path
import requests
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, StreamingResponse
import streamlit.web.bootstrap as bootstrap
import threading
import time
import subprocess
from contextlib import asynccontextmanager
import asyncio
import websockets

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Streamlit in a separate process
    streamlit_process = subprocess.Popen([
        "streamlit", "run",
        str(project_root / "frontend" / "app.py"),
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true"
    ])
    # Wait for Streamlit to start
    time.sleep(5)
    yield
    # Cleanup
    streamlit_process.terminate()

app = FastAPI(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
async def root():
    # Proxy the request to Streamlit
    response = requests.get("http://localhost:8501")
    return response.text

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.websocket("/_stcore/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async with websockets.connect("ws://localhost:8501/_stcore/stream") as streamlit_ws:
            while True:
                try:
                    # Forward messages from Streamlit to client
                    streamlit_message = await streamlit_ws.recv()
                    await websocket.send_text(streamlit_message)
                except websockets.exceptions.ConnectionClosed:
                    break
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
    finally:
        await websocket.close()

@app.get("/{path:path}")
async def proxy_streamlit(path: str, request: Request):
    # Forward all other requests to Streamlit
    streamlit_url = f"http://localhost:8501/{path}"
    response = requests.get(streamlit_url, params=request.query_params)
    return StreamingResponse(
        response.iter_content(chunk_size=1024),
        media_type=response.headers.get("content-type", "text/html")
    ) 