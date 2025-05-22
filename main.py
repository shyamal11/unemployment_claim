import os
import subprocess
import sys

def start_streamlit():
    cmd = [
        "streamlit", "run",
        "frontend/app.py",
        "--server.port=" + os.environ.get("PORT", "8501"),
        "--server.address=0.0.0.0",
        "--server.headless=true"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    start_streamlit() 