import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.schemas import AnalyzeRequest, AnalyzeResponse
from backend.services.analysis_service import analyze_url
from backend.ml.model_loader import load_model
from backend.config import ROOT, SCREENSHOT_DIRECTORY

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
app = FastAPI(title="AI/ML Phishing Domain Detector")
app.mount("/static", StaticFiles(directory=ROOT / "frontend"), name="static")
app.mount("/screenshots", StaticFiles(directory=SCREENSHOT_DIRECTORY), name="screenshots")

@app.get("", include_in_schema=False)
def home(): return FileResponse(ROOT / "frontend" / "index.html")

@app.get("/health")
def health(): return {"status": "ok", "model_loaded": load_model() is not None}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    try: return analyze_url(str(request.url))
    except ValueError as error: raise HTTPException(400, str(error)) from error
    except RuntimeError as error: raise HTTPException(503, str(error)) from error
    except Exception as error:
        logging.exception("Analysis failed")
        raise HTTPException(500, "Analysis could not be completed safely.") from error
