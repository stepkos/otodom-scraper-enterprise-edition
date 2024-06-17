import csv

from modules.apartments.models import ApartmentDetails

apartment_headers = [
    "title",
    "address",
    "price",
    "rooms",
    "area",
    "floor",
]

details_headers = [
    "max_floor",
    "rent",
    "energy_certificate",
    "form_of_the_property",
    "finishing_condition",
    "balcony_garden_terrace",
    "parking_place",
    "heating",
    "market",
    "advertisement_type",
    "year_of_construction",
    "type_of_development",
    "windows",
    "is_elevator",
]


def export():
    details = ApartmentDetails.objects.all()
    with open("apartments-wroclaw.csv", "w", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=apartment_headers + details_headers, delimiter=";"
        )
        writer.writeheader()

        counter = 0
        for detail in details:
            counter += 1
            writer.writerow(
                {
                    "title": detail.apartment.title,
                    "address": detail.apartment.address,
                    "price": detail.apartment.price,
                    "rooms": detail.apartment.rooms,
                    "area": detail.apartment.area,
                    "floor": detail.apartment.floor,
                    "max_floor": detail.max_floor,
                    "rent": detail.rent,
                    "energy_certificate": detail.energy_certificate,
                    "form_of_the_property": detail.form_of_the_property,
                    "finishing_condition": detail.finishing_condition,
                    "balcony_garden_terrace": detail.balcony_garden_terrace,
                    "parking_place": detail.parking_place,
                    "heating": detail.heating,
                    "market": detail.market,
                    "advertisement_type": detail.advertisement_type,
                    "year_of_construction": detail.year_of_construction,
                    "type_of_development": detail.type_of_development,
                    "windows": detail.windows,
                    "is_elevator": detail.is_elevator,
                }
            )

        print(f"Exported {counter} apartments.")
