import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List
import os
import json

class SimpleMLP(nn.Module):
    def __init__(self, input_dim: int = 4, hidden: int = 32):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden)
        self.fc2 = nn.Linear(hidden, hidden)
        self.out = nn.Linear(hidden, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return torch.sigmoid(self.out(x))

class ModelEngine:
    def __init__(self, model: nn.Module):
        self.model = model
        self.model.eval()

    @classmethod
    def load_from_path(cls, path: str):
        # If model doesn't exist, instantiate a default untrained model
        if os.path.exists(path):
            try:
                state = torch.load(path, map_location='cpu')
                model = SimpleMLP(input_dim=state.get('input_dim', 4))
                model.load_state_dict(state['state_dict'])
            except Exception:
                model = SimpleMLP()
        else:
            model = SimpleMLP()
        return cls(model)

    def predict(self, features: List[float]) -> float:
        with torch.no_grad():
            t = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
            out = self.model(t).item()
            return float(out)

    def featurize(self, tx: dict) -> List[float]:
        # Simple featurization: normalized value, gas, input length, time-of-day
        value = float(tx.get('value', 0))
        gas = float(tx.get('gas', 0))
        input_len = float(len(tx.get('input', '') or ''))
        ts = float(tx.get('timestamp', 0)) % 86400
        return [value / (10**18 + 1), gas / (10**6 + 1), input_len / 1024.0, ts / 86400.0]

    def save(self, path: str):
        data = {'state_dict': self.model.state_dict(), 'input_dim': self.model.fc1.in_features}
        torch.save(data, path)
