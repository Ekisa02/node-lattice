import pytest
from app.core.model import SimpleMLP, ModelEngine
import torch

def test_model_forward():
    model = SimpleMLP(input_dim=4)
    engine = ModelEngine(model)
    features = [0.1, 0.2, 0.3, 0.4]
    score = engine.predict(features)
    assert 0.0 <= score <= 1.0
