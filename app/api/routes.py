from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from ..schemas import IngestRequest, PredictRequest, PredictResponse, HealthResponse
from ..core.chain_adapter import ChainAdapter
from ..core.model import ModelEngine
from ..core.storage import init_db, save_transaction, save_prediction, get_metrics
from ..config import settings
import asyncio

router = APIRouter()

@router.on_event('startup')
async def _init():
    await init_db()

@router.get('/health', response_model=HealthResponse)
async def health(request: Request):
    model_loaded = hasattr(request.app.state, 'model_engine') and isinstance(request.app.state.model_engine, ModelEngine)
    return HealthResponse(status='ok' if model_loaded else 'degraded', model_loaded=model_loaded)

@router.post('/ingest')
async def ingest(payload: IngestRequest, background_tasks: BackgroundTasks, request: Request):
    # Save raw transaction and schedule scoring in background
    tx = payload.dict()
    tx_id = await save_transaction(tx)

    # offload scoring to background
    background_tasks.add_task(_score_and_store, request.app.state.model_engine, tx_id, tx)
    return JSONResponse({'status': 'accepted', 'tx_id': tx_id})

async def _score_and_store(model_engine: ModelEngine, tx_id: int, tx: dict):
    # Extract a simple feature vector for demo purposes
    features = model_engine.featurize(tx)
    score = model_engine.predict(features)
    await save_prediction(tx_id, score, features)

@router.post('/predict', response_model=PredictResponse)
async def predict(payload: PredictRequest, request: Request):
    model_engine: ModelEngine = request.app.state.model_engine
    features = payload.features
    score = model_engine.predict(features)
    return PredictResponse(score=float(score), tags=['anomaly' if score > 0.5 else 'normal'])

@router.get('/metrics')
async def metrics():
    return await get_metrics()
