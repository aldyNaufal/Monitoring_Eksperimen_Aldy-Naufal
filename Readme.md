Bukti Serving Model via Docker & Monitoring
==========================================

1. Pull image model dari Docker Hub
-----------------------------------
Image model disimpan di Docker Hub:

- Image name : aldy2802/genre-game-model:latest
- URL        : https://hub.docker.com/r/aldy2802/genre-game-model

Perintah yang dijalankan di terminal:

docker pull aldy2802/genre-game-model:latest


2. Menjalankan network Docker untuk monitoring
----------------------------------------------
Network khusus untuk menghubungkan model, Prometheus, dan Grafana:

docker network create monitoring


3. Menjalankan container model (FastAPI + /predict + /metrics)
--------------------------------------------------------------
Container model dijalankan dari image Docker Hub:

docker run -d --name genre-game-api --network monitoring -p 8000:8000 aldy2802/genre-game-model:latest

Verifikasi container berjalan:

docker ps

Hasilnya menunjukkan 3 container aktif:
- genre-game-api  (image: aldy2802/genre-game-model:latest, port 8000:8000)
- prometheus      (image: prom/prometheus, port 9090:9090)
- grafana         (image: grafana/grafana, port 3300:3000)


4. Menjalankan Prometheus
-------------------------
Prometheus dijalankan dengan konfigurasi scrape ke service model:

File prometheus.yml:

global:
  scrape_interval: 5s
  evaluation_interval: 5s

scrape_configs:
  - job_name: "genre_game_inference"
    metrics_path: /metrics
    static_configs:
      - targets: ["genre-game-api:8000"]
        labels:
          service: "genre_game_inference"

Perintah menjalankan Prometheus:

docker run -d --name prometheus --network monitoring \
  -p 9090:9090 \
  -v ./prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

Prometheus UI dapat diakses di:
http://localhost:9090

Pada menu /targets, target "genre-game-api:8000" tampil dengan status UP.


5. Menjalankan Grafana
----------------------
Grafana digunakan untuk visualisasi metrik dari Prometheus.

Perintah menjalankan Grafana:

docker run -d --name grafana --network monitoring \
  -p 3300:3000 \
  grafana/grafana

Grafana UI dapat diakses di:
http://localhost:3300

Data source Prometheus ditambahkan dengan URL:
http://prometheus:9090

Dashboard dibuat untuk menampilkan:
- Request rate (app_inference_requests_total)
- Total prediction per genre (app_inference_prediction_per_genre)
- Queue length (app_inference_queue_length)
- Last confidence (app_inference_last_confidence)
- Time since last prediction (app_inference_seconds_since_last_prediction)


6. Menguji endpoint /predict dari container model
-------------------------------------------------
Model diekspos melalui FastAPI dengan endpoint POST /predict.

Contoh pengujian dari PowerShell:

Invoke-RestMethod -Uri "http://localhost:8000/predict" `
  -Method POST `
  -ContentType "application/json" `
  -Body (@{ title="valorant clutch 1v5"; description=""; tags="valorant fps" } | ConvertTo-Json)

Respons yang diterima (contoh):

{
  "predicted_genre": "FPS",
  "model_version": "1.0"
}


7. Menginjeksi traffic otomatis menggunakan traffic_generator.py
----------------------------------------------------------------
Untuk menghasilkan trafik kontinu ke endpoint /predict, dijalankan script:

python traffic_generator.py

Script ini akan mengirim request POST ke:
http://localhost:8000/predict

dengan payload acak berisi kombinasi (title, description, tags) berbagai game, misalnya:

{
  "title": "Valorant clutch 1v5 di overtime",
  "description": "Main ranked solo queue",
  "tags": "valorant fps shooter"
}

Di terminal terlihat log seperti:

0 200 {'predicted_genre': 'FPS', 'model_version': '1.0'}
1 200 {'predicted_genre': 'MOBA', 'model_version': '1.0'}
2 200 {'predicted_genre': 'Battle Royale', 'model_version': '1.0'}
...

Selama traffic_generator.py berjalan:
- Prometheus secara periodik melakukan GET /metrics ke genre-game-api.
- Dashboard Grafana menampilkan grafik metrik yang terus bergerak (request rate, total prediksi per genre, dll).


Ringkasan
--------
- Model berhasil di-pull dari Docker Hub dan dijalankan sebagai container genre-game-api.
- Container model, Prometheus, dan Grafana berjalan bersamaan di network monitoring.
- Endpoint /predict dari container digunakan untuk inference.
- Endpoint /metrics dari container di-scrape oleh Prometheus.
- Traffic dari traffic_generator.py memicu perubahan metrik yang divisualisasikan di Grafana.
