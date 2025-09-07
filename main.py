# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import subprocess, os, sys, time

app = FastAPI()

# Dossier des exports vidéo
ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "out"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Optionnel : servir les fichiers directement via /out/<nom>.mp4
app.mount("/out", StaticFiles(directory=str(OUT_DIR)), name="out")

@app.get("/")
def home():
    return {"status": "running", "message": "YouTube Shorts API is live"}

@app.get("/list")
def list_files():
    """Liste les dernières vidéos générées dans out/ (nom, taille, date)."""
    files = []
    for p in OUT_DIR.glob("*.mp4"):
        try:
            files.append({
                "name": p.name,
                "size_bytes": p.stat().st_size,
                "mtime": p.stat().st_mtime
            })
        except Exception:
            pass
    files.sort(key=lambda x: x["mtime"], reverse=True)
    for f in files:
        f["mtime_human"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(f["mtime"]))
    return {"files": files[:20]}

@app.post("/run")
def run_script():
    """
    Lance collect_youtube_shorts.py et renvoie stdout/stderr + code retour.
    Assure-toi que ton script écrit la sortie finale dans OUT_DIR (./out).
    """
    try:
        cmd = [sys.executable, "collect_youtube_shorts.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        # Log dans Render
        print("=== STDOUT ===\n", result.stdout)
        print("=== STDERR ===\n", result.stderr)
        return {
            "status": "ok" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}