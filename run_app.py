import os
import subprocess
import webbrowser
import time
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT, "backend")
FRONTEND_DIR = os.path.join(ROOT, "frontend")

def run_backend():
    print("Starting FastAPI backend on port 8000...")
    return subprocess.Popen(
        ["python", "-m", "uvicorn", "app:app", "--reload", "--port", "8000"],
        cwd=BACKEND_DIR
    )

def run_frontend():
    print("Starting frontend on port 5500...")
    return subprocess.Popen(
        ["python", "-m", "http.server", "5500"],
        cwd=FRONTEND_DIR
    )

if __name__ == "__main__":
    print("Launching Shelter Finder app...")

    backend = run_backend()
    time.sleep(2)  # Give backend time to boot

    frontend = run_frontend()
    time.sleep(1)

    url = "http://127.0.0.1:5500/index.html"
    print(f"Opening browser at {url}")
    webbrowser.open(url)

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend.terminate()
        frontend.terminate()
        sys.exit(0)
