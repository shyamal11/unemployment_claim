from http.server import HTTPServer, BaseHTTPRequestHandler
import streamlit.web.bootstrap as bootstrap
import sys
import os
import threading
import time

def run_streamlit():
    sys.argv = ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
    bootstrap.run()

class StreamlitHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Streamlit app is running")

def run_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get('PORT', 8080))), StreamlitHandler)
    server.serve_forever()

if __name__ == "__main__":
    # Start Streamlit in a separate thread
    streamlit_thread = threading.Thread(target=run_streamlit)
    streamlit_thread.daemon = True
    streamlit_thread.start()
    
    # Give Streamlit time to start
    time.sleep(2)
    
    # Start the HTTP server
    run_server() 