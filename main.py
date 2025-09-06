
from fastapi import FastAPI
import subprocess, os, sys

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running", "message": "YouTube Shorts API is live"}

@app.post("/run")
def run_script():
    try:
        cmd = [sys.executable, "collect_youtube_shorts.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return {
            "status": "ok" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}