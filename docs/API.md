# API Reference

GET /health
- Returns: status and whether model is loaded.

POST /ingest
- Body: IngestRequest (hash, from_addr, to_addr, value, gas, timestamp, input optional)
- Response: {status: 'accepted', tx_id: <int>}

POST /predict
- Body: {features: [float]}
- Response: {score: float, tags: [string]}

GET /metrics
- Returns transaction and prediction counts.
