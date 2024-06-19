__all__ = ["mlp", "scaler_in", "scaler_out"]

from pathlib import Path

import joblib
import torch

from modules.valuations.ml.net import MLP

model_path = Path(__file__).parent / "models" / "estimate-wro-aparts-mlp.pth"
scaler_x_path = (
    Path(__file__).parent / "scalers" / "estimate-wro-aparts-mlp-xscaler.pkl"
)
scaler_y_path = (
    Path(__file__).parent / "scalers" / "estimate-wro-aparts-mlp-yscaler.pkl"
)

mlp = MLP()
mlp.load_state_dict(torch.load(str(model_path)))
mlp.eval()

scaler_in = joblib.load(str(scaler_x_path))
scaler_out = joblib.load(str(scaler_y_path))
