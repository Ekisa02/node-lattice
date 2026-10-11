import asyncio
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router as api_router
from .core.model import ModelEngine
from .config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("node-lattice")

app = FastAPI(title="Node Lattice", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
async def startup_event():
    # Initialize model engine and attach to app state
    app.state.model_engine = ModelEngine.load_from_path(settings.MODEL_PATH)
    logger.info("Model engine loaded")
    # Optionally start background tasks (e.g., streaming ingestion)
    # Example: app.state.ingest_task = asyncio.create_task(background_streamer())

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Node Lattice")
    # Cancel background tasks if necessary

app.include_router(api_router, prefix="")
