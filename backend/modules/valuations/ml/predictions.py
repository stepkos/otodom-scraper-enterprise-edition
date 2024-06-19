import torch

from modules.valuations.ml import mlp, scaler_in, scaler_out


def predict_raw(input_data: list[float]) -> float:
    assert len(input_data) == 19, "Input data must have 19 elements"

    with torch.no_grad():
        return mlp(torch.tensor(input_data, dtype=torch.float32)).item()


def predict_with_scalers(input_data: list[float]) -> float:
    assert len(input_data) == 19, "Input data must have 19 elements"

    with torch.no_grad():
        in_scaled = scaler_in.transform([input_data])
        in_tensor = torch.tensor(in_scaled, dtype=torch.float32)
        out_numpy = mlp(in_tensor).detach().numpy()
        return scaler_out.inverse_transform(out_numpy).item()
