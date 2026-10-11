# Node Lattice

Node Lattice is a modular Web3 infrastructure toolkit: a FastAPI-based service that ingests chain data, scores transactions using a PyTorch model (anomaly / fraud scoring), and provides endpoints and background workflows for retraining and analytics.

Key features

- FastAPI HTTP API for ingestion, prediction, and metrics
- PyTorch model integration for transaction scoring and incremental retraining
- Chain adapter to fetch data from EVM-compatible nodes (Web3.py)
- Async storage with SQLAlchemy + aiosqlite for persistence
- Background tasks for streaming ingestion and scheduled retraining
- Tests and development scripts

Architecture

Components:
- API Layer (FastAPI): HTTP endpoints, validation, and request routing.
- ML Engine (PyTorch): lightweight model for scoring transactions and retraining entry points.
- Chain Adapter: Web3.py-based connector to pull transactions and block data.
- Storage: Async SQLite via SQLAlchemy (async engine) storing transactions and predictions.
- Background Worker: Async tasks for streaming ingestion and periodic retraining.

Installation

Requirements: Python 3.9+

1. Clone

```bash
git clone https://github.com/yourorg/node-lattice.git
cd node-lattice
```

2. Create virtualenv and install

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Set environment variables (copy .env.example -> .env)

```bash
cp .env.example .env
# Edit .env to set DATABASE_URL and WEB3_HTTP_PROVIDER
```

4. Initialize DB (simple auto-create on first run) and start server

```bash
uvicorn app.main:app --reload
```

Usage examples

- Health check:

```bash
curl http://localhost:8000/health
```

- Ingest a transaction (POST /ingest):

```bash
curl -X POST http://localhost:8000/ingest -H "Content-Type: application/json" -d '{"hash":"0xabc...","from_addr":"0x1","to_addr":"0x2","value":1000000000000000000,"gas":21000,"timestamp": 1620000000}'
```

- Predict from features (POST /predict):

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"features":[0.1,0.2,0.3,0.4]}'
```

Development

- Run tests:

```bash
pytest -q
```

- Train a sample model (example script):

```bash
python scripts/train_model.py --output models/sample_model.pt
```

Project Layout

- app/: application package with API, core, db, and tasks
- scripts/: convenience scripts (training example)
- tests/: pytest test cases
- models/: saved model artifacts (ignored from Git)
- docs/: human documentation

Contributing

Contributions welcome: open an issue, propose an architecture change, or submit a pull request with tests.

License

This repository is provided under the MIT License. See LICENSE for details.
