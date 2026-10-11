# Architecture

Node Lattice is organized as follows:

- API (FastAPI): exposes endpoints to ingest transactions, predict scores, inspect health, and retrieve metrics.
- ML Engine (PyTorch): provides featurization, prediction, and model persistence APIs.
- Chain Adapter: thin wrapper around Web3.py to fetch chain data.
- Storage (Async SQLAlchemy): stores raw transactions and predictions for traceability.
- Tasks: background and scheduled jobs for streaming ingestion and retraining.

Data flow

1. External client posts a transaction to /ingest.
2. API saves the transaction to storage and enqueues a background scoring job.
3. Background job featurizes the transaction, runs the model to produce a score, and saves the prediction.
4. Retraining is performed offline using scripts or scheduled tasks that update the model artifact used on startup.
