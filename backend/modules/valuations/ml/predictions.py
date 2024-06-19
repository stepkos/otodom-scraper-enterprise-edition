import torch

from modules.valuations.ml import trained_mlp


def predict_raw(input_data: list[float]) -> float:
    assert len(input_data) == 19, "Input data must have 19 elements"

    with torch.no_grad():
        return trained_mlp(torch.tensor(input_data, dtype=torch.float32)).item()
