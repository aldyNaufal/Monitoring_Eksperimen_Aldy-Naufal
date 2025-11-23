# 7.inference.py

from pathlib import Path
import time
import joblib
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import Response

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# IMPORT semua metric dari prometheus_exporter.py
from prometheus_exporter import (
    INFERENCE_REQUEST_TOTAL,
    INFERENCE_LATENCY_SECONDS,
    INFERENCE_IN_PROGRESS,
    INFERENCE_PREDICTION_PER_GENRE,
    INFERENCE_REQUEST_SIZE,
    INFERENCE_LAST_CONFIDENCE,
    INFERENCE_LAST_PREDICTION_TS,
    INFERENCE_ERROR_TOTAL,
    INFERENCE_QUEUE_LENGTH,
    INFERENCE_MODEL_VERSION,
)

# ====== 1. Load model ======

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "tfidf_svc_genre_game_basic.pkl"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model tidak ditemukan di {MODEL_PATH}")

model = joblib.load(MODEL_PATH)

# set model version (label version="1.0")
INFERENCE_MODEL_VERSION.labels(version="1.0").set(1)

# ====== 2. FastAPI app ======

app = FastAPI(
    title="Genre Game Inference Service",
    description="Service untuk memprediksi genre game + expose Prometheus metrics",
    version="1.0.0",
)


class InferenceRequest(BaseModel):
    title: str
    description: str | None = ""
    tags: str | None = ""


class InferenceResponse(BaseModel):
    predicted_genre: str
    model_version: str = "1.0"


def _combine_text(req: InferenceRequest) -> str:
    parts = [req.title]
    if req.description:
        parts.append(req.description)
    if req.tags:
        parts.append(req.tags)
    return " ".join(parts)


# ====== 3. Endpoint metrics ======

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


# ====== 4. Endpoint healthcheck ======

@app.get("/health")
def health():
    return {"status": "ok"}


# ====== 5. Endpoint inference ======

@app.post("/predict", response_model=InferenceResponse)
def predict(request: InferenceRequest):
    start_time = time.time()
    endpoint = "/predict"

    # mulai hitung request in-progress & queue (dummy)
    INFERENCE_IN_PROGRESS.inc()
    INFERENCE_QUEUE_LENGTH.set(0)

    try:
        text = _combine_text(request)

        # ukuran input
        INFERENCE_REQUEST_SIZE.observe(len(text))

        # inference
        y_pred = model.predict([text])[0]

        # latency
        latency = time.time() - start_time
        INFERENCE_LATENCY_SECONDS.labels(endpoint=endpoint).observe(latency)

        # request success
        INFERENCE_REQUEST_TOTAL.labels(endpoint=endpoint, status="success").inc()

        # count per-genre
        INFERENCE_PREDICTION_PER_GENRE.labels(genre=y_pred).inc()

        # dummy confidence & timestamp
        INFERENCE_LAST_CONFIDENCE.set(1.0)
        INFERENCE_LAST_PREDICTION_TS.set(time.time())

        return InferenceResponse(predicted_genre=y_pred, model_version="1.0")

    except Exception as e:
        # catat error ke metric
        INFERENCE_REQUEST_TOTAL.labels(endpoint=endpoint, status="error").inc()
        INFERENCE_ERROR_TOTAL.labels(type=e.__class__.__name__).inc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        INFERENCE_IN_PROGRESS.dec()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
