FROM python:3.11-slim

# 1. Workdir di dalam container
WORKDIR /app

# 2. Copy requirements (kalau ada)
# kalau kamu punya requirements.txt untuk inference + prometheus
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy semua kode inference + model
COPY . .

# 4. Pastikan path model sama dengan di inference.py
# MODEL_PATH = BASE_DIR / "models" / "tfidf_svc_genre_game_best_tuned_local.pkl"
# jadi di host, pastikan ada folder models/ dan file .pkl ini di dalamnya

# 5. Jalankan uvicorn saat container start
CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8000"]
