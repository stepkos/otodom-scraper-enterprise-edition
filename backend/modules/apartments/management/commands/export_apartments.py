import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from modules.apartments.models import ApartmentDetails


class Command(BaseCommand):
    help = "Export apartments with details to CSV file."

    APARTMENT_HEADERS = [
        "title",
        "address",
        "price",
        "rooms",
        "area",
        "floor",
    ]
    DETAILS_HEADERS = [
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
    ALL_HEADERS = APARTMENT_HEADERS + DETAILS_HEADERS
    EXPORT_BASE_PATH = Path(__file__).parent.parent / "exports"

    def add_arguments(self, parser):
        parser.add_argument(
            "-f", "--filename",
            type=str,
            required=True,
            help="The name of the output CSV file"
        )

    def handle(self, *args, **options):
        details = ApartmentDetails.objects.all()
        export_file = self.EXPORT_BASE_PATH / options["filename"]
        with export_file.open("w", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file, fieldnames=self.ALL_HEADERS, delimiter=";"
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

            self.stdout.write(
                self.style.SUCCESS(f"Exported {counter} apartments.")
            )
