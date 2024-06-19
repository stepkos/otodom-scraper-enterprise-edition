import random

from modules.apartments.models import Apartment, ApartmentDetails


def fetch_predict_attrs(apartment: Apartment) -> dict | None:
    if not hasattr(apartment, "details") or not apartment.details:
        return None

    return {
        "rooms": apartment.rooms,
        "area": apartment.area,
        "address_estate": apartment.address_estate,
        "floor": apartment.floor,
        "max_floor": apartment.details.max_floor,
        "market": apartment.details.market,
        "year_of_construction": apartment.details.year_of_construction,
        "finishing_condition": apartment.details.finishing_condition,
        "is_elevator": apartment.details.is_elevator
    }


def check_is_not_none(apartment_dict: dict, acceptable_nones: list = None) -> bool:
    acceptable_nones = acceptable_nones or []
    for key, value in apartment_dict.items():
        if key not in acceptable_nones and value is None:
            return False
    return True


unexpected_values_dict = {
    "floor": ["poddasze", "suterena"],
}

expected_values_dict = {
    "address_estate": [
        'Fabryczna',
        'Krzyki',
        'Śródmieście',
        'Stare Miasto',
        'Psie Pole',
        'Kobierzyce',
        'Siechnice',
        'Miękinia',
        'Długołęka'
    ],
    "market": ["pierwotny", "wtórny"],
    "finishing_condition": ["do wykończenia", "do zamieszkania", "do remontu"],
}


def check_is_not_unexpected_values(apartment_dict: dict, unexpected_values: dict, expected_values: dict) -> bool:
    for key, value in apartment_dict.items():
        if key in unexpected_values and value in unexpected_values[key]:
            return False
        if key in expected_values and value not in expected_values[key]:
            return False
    return True


def cast_values(apartment_dict: dict) -> dict:
    if apartment_dict["floor"] == "parter":
        apartment_dict["floor"] = 0
    elif apartment_dict["floor"] == "10+":
        apartment_dict["floor"] = int(apartment_dict['max_floor']) // 2

    apartment_dict["floor"] = int(apartment_dict["floor"])
    apartment_dict["max_floor"] = int(apartment_dict["max_floor"])
    apartment_dict["year_of_construction"] = int(apartment_dict["year_of_construction"])
    apartment_dict["rooms"] = int(apartment_dict["rooms"])
    apartment_dict["area"] = float(apartment_dict["area"])

    return apartment_dict


def check_skrajne_wartosci(apartment_dict: dict) -> bool:
    # do implemetnacji na podstwie
    # data_cut = data_cleaned.copy()
    # data_cut = data_cut[data_cut['price'] < 2000000]
    # data_cut = data_cut[data_cut['year_of_construction'] > 1850]
    # data_cut = data_cut[data_cut['year_of_construction'] < 2030]
    # data_cut = data_cut[data_cut['max_floor'] < 30]
    # data_cut = data_cut[data_cut['area'] < 200]
    return True


address_estate_to_codes = {
    'Fabryczna': 1,
    'Krzyki': 3,
    'Śródmieście': 8,
    'Stare Miasto': 7,
    'Psie Pole': 5,
    'Kobierzyce': 2,
    'Siechnice': 6,
    'Miękinia': 4,
    'Długołęka': 0,
}

market_to_codes = {
    'wtórny': 1,
    'pierwotny': 0,
}

finishing_condition_to_codes = {
    'do wykończenia': 1,
    'do zamieszkania': 2,
    'do remontu': 0,
}

is_elevator_to_codes = {
    True: 1,
    False: 0,
}


def cast_categories_to_codes(apartment_dict: dict) -> dict:
    apartment_dict["address_estate"] = address_estate_to_codes[apartment_dict["address_estate"]]
    apartment_dict["market"] = market_to_codes[apartment_dict["market"]]
    apartment_dict["finishing_condition"] = finishing_condition_to_codes[apartment_dict["finishing_condition"]]
    apartment_dict["is_elevator"] = is_elevator_to_codes[apartment_dict["is_elevator"]]
    return apartment_dict


def one_hot_encode(apartment_dict: dict) -> dict:
    # dla finishing_condition oraz address_estate
    for i in range(max(finishing_condition_to_codes.values()) + 1):
        apartment_dict[f"finishing_condition_{i}"] = 0 if i != apartment_dict["finishing_condition"] else 1

    for i in range(max(address_estate_to_codes.values()) + 1):
        apartment_dict[f"address_estate_{i}"] = 0 if i != apartment_dict["address_estate"] else 1

    del apartment_dict["finishing_condition"]
    del apartment_dict["address_estate"]

    return apartment_dict


def processing_apartment(apartment: Apartment) -> dict | None:
    apartment_dict = fetch_predict_attrs(apartment)
    if not apartment_dict:
        return None

    # uzupelniamy null srednia tam gdzie mozemy
    # apartment_dict["is_elevator"] = apartment_dict["is_elevator"] or 0.5780
    # apartment_dict["market"] = apartment_dict["market"] or 0.5860

    apartment_dict["is_elevator"] = (
        apartment_dict["is_elevator"] or random.choice([False, True])
    )
    apartment_dict["market"] = (
            apartment_dict["market"] or random.choice(["pierwotny", "wtórny"])
    )
    apartment_dict["finishing_condition"] = (
        apartment_dict["finishing_condition"] or random.choice(
            ["do wykończenia", "do zamieszkania", "do remontu"]
        )
    )

    if not all([
        check_is_not_none(apartment_dict),
        check_is_not_unexpected_values(apartment_dict, unexpected_values_dict, expected_values_dict)
    ]):
        return None

    apartment_dict = cast_values(apartment_dict)
    apartment_dict = cast_categories_to_codes(apartment_dict)
    apartment_dict = one_hot_encode(apartment_dict)
    return apartment_dict

