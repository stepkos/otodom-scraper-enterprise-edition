from pathlib import Path

import torch

from modules.valuations.ml.net import MLP

model_path = Path(__file__).parent / "models" / "estimate-wro-aparts-mlp.pth"

trained_mlp = MLP()
trained_mlp.load_state_dict(torch.load(str(model_path)))
trained_mlp.eval()
