# 3.prometheus_exporter.py

from prometheus_client import Counter, Histogram, Gauge

# Total request inference
INFERENCE_REQUEST_TOTAL = Counter(
    "app_inference_requests_total",
    "Total number of inference requests",
    ["endpoint", "status"],
)

# Waktu respon inference (detik)
INFERENCE_LATENCY_SECONDS = Histogram(
    "app_inference_latency_seconds",
    "Inference latency in seconds",
    ["endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5],
)

# Berapa banyak request yang sedang diproses
INFERENCE_IN_PROGRESS = Gauge(
    "app_inference_in_progress",
    "Number of inference requests in progress",
)

# Count per-genre (berapa kali genre ini diprediksi)
INFERENCE_PREDICTION_PER_GENRE = Counter(
    "app_inference_prediction_per_genre_total",
    "Total predictions per genre",
    ["genre"],
)

# Ukuran payload input (panjang karakter teks)
INFERENCE_REQUEST_SIZE = Histogram(
    "app_inference_request_size_chars",
    "Length of input text (characters)",
    buckets=[50, 100, 200, 400, 800, 1600, 3200],
)

# Confidence last prediction (dummy / jika nanti kamu pakai probabilitas)
INFERENCE_LAST_CONFIDENCE = Gauge(
    "app_inference_last_confidence",
    "Confidence of last prediction (0–1)",
)

# Timestamp unix dari last successful prediction
INFERENCE_LAST_PREDICTION_TS = Gauge(
    "app_inference_last_prediction_ts",
    "Unix timestamp of last successful prediction",
)

# Total error
INFERENCE_ERROR_TOTAL = Counter(
    "app_inference_error_total",
    "Total errors during inference",
    ["type"],
)

# Dummy queue length (boleh kamu isi 0 atau di-improve)
INFERENCE_QUEUE_LENGTH = Gauge(
    "app_inference_queue_length",
    "Simulated inference queue length",
)

# Versi model (diset 1.0, 2.0, dst)
INFERENCE_MODEL_VERSION = Gauge(
    "app_inference_model_version",
    "Deployed model version",
    ["version"],
)
