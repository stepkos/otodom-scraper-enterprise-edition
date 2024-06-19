import torch

from modules.valuations.ml import mlp, scaler_in, scaler_out
from modules.valuations.pre_processor import processing_apartment


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


attributes = [
    'rooms', 'area', 'floor', 'max_floor', 'market', 'year_of_construction',
    'is_elevator', 'finishing_condition_0',
    'finishing_condition_1', 'finishing_condition_2', 'address_estate_0',
    'address_estate_1', 'address_estate_2', 'address_estate_3',
    'address_estate_4', 'address_estate_5', 'address_estate_6',
    'address_estate_7', 'address_estate_8'
]


def predict_with_scalers_from_dict(dict_data: dict[str, int]) -> float:
    input_data = [dict_data[attr] for attr in attributes]
    return predict_with_scalers(input_data)


def predict_with_scalers_from_apartment(apartment) -> float | None:
    data = processing_apartment(apartment)
    if data is None:
        return None
    return predict_with_scalers_from_dict(data)
