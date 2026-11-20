#!/usr/bin/env bash
PORT="${PORT:-8501}"
echo "Starting Streamlit application on host 0.0.0.0 and port $PORT..."
exec streamlit run app.py \
  --server.port "$PORT" \
  --server.address 0.0.0.0 \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  --browser.gatherUsageStats false

