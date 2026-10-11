from pydantic import BaseModel, Field
from typing import List, Optional

class IngestRequest(BaseModel):
    hash: str
    from_addr: str
    to_addr: str
    value: int
    gas: int
    timestamp: int
    input: Optional[str] = None

class PredictRequest(BaseModel):
    features: List[float]

class PredictResponse(BaseModel):
    score: float
    tags: List[str]

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
