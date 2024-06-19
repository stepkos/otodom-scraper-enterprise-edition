from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
from yarl import URL

from modules.apartments.constants import (
    ApartmentStatus,
    FinishingConditionChoice,
    FloorChoice,
    MarketChoice,
)
from modules.apartments.models import Apartment, ApartmentDetails


class ApartmentModelTests(TestCase):

    def setUp(self):
        self.apartment = Apartment.objects.create(
            title="Test Apartment",
            address="Przedmieście Świdnickie, Stare Miasto, Wrocław, dolnośląskie",
            price=Decimal("500000"),
            subpage="/test-apartment",
            rooms=3,
            area=Decimal("100.00"),
            floor=FloorChoice.GROUND_FLOOR,
            status=ApartmentStatus.VALUATED,
            estimated_price=Decimal("550000"),
        )

    def test_apartment_creation(self):
        self.assertEqual(self.apartment.title, "Test Apartment")
        self.assertEqual(self.apartment.price, Decimal("500000"))
        self.assertEqual(self.apartment.estimated_price, Decimal("550000"))
        self.assertEqual(self.apartment.status, ApartmentStatus.VALUATED)

    def test_address_estate(self):
        self.assertEqual(self.apartment.address_estate, "StareMiasto")

    def test_price_per_m2(self):
        self.assertEqual(self.apartment.price_per_m2, 5000.00)

    def test_below_market_price(self):
        self.assertEqual(
            (float(self.apartment.estimated_price) - float(self.apartment.price)), 50000
        )
        self.assertEqual(self.apartment.below_market_price, 50000)

    def test_is_special_offer(self):
        self.assertTrue(self.apartment.is_special_offer(40000))
        self.assertFalse(self.apartment.is_special_offer(60000))

    def test_str(self):
        self.assertEqual(
            str(self.apartment), "Apartment(title=Test Apartment, price=500000)"
        )

    def test_get_abs_details_url(self):
        self.assertEqual(
            self.apartment.subpage_abs_path,
            URL("https://www.otodom.pl/test-apartment"),
        )


class ApartmentDetailsModelTests(TestCase):

    def setUp(self):
        self.apartment = Apartment.objects.create(
            title="Test Apartment", subpage="/test-apartment"
        )
        self.details = ApartmentDetails.objects.create(
            apartment=self.apartment,
            exact_floor=2,
            exact_rooms=3,
            max_floor=5,
            rent=2000,
            energy_certificate="A",
            form_of_the_property="Ownership",
            finishing_condition=FinishingConditionChoice.TO_RENOVATE,
            balcony_garden_terrace="Balcony",
            parking_place="Garage",
            heating="Central",
            description="Spacious and modern apartment.",
            market=MarketChoice.PRIMARY,
            advertisement_type="Sale",
            year_of_construction=2020,
            type_of_development="Residential",
            windows="Double-glazed",
            is_elevator=True,
        )

    def test_apartment_details_creation(self):
        self.assertEqual(self.details.apartment, self.apartment)
        self.assertEqual(self.details.exact_floor, 2)
        self.assertEqual(
            self.details.finishing_condition, FinishingConditionChoice.TO_RENOVATE
        )

    def test_str(self):
        self.assertEqual(
            str(self.details), "Apartment(title=Test Apartment, price=None) - details"
        )
