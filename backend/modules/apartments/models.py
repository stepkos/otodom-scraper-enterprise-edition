from contextlib import suppress

from django.db import models
from django.utils.translation import gettext_lazy as _
from yarl import URL

from modules.apartments.constants import (
    ApartmentStatus,
    FinishingConditionChoice,
    FloorChoice,
    MarketChoice, OTODOM_BASE_URL,
)
from modules.core.models import BaseModel


class Apartment(BaseModel):
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    address = models.CharField(
        verbose_name=_("Address"), max_length=255, blank=True, null=True
    )
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=10, decimal_places=0, blank=True, null=True
    )
    subpage = models.URLField(verbose_name=_("Subpage"), unique=True, editable=False)
    rooms = models.PositiveSmallIntegerField(
        verbose_name=_("Rooms"),
        blank=True,
        null=True,
        help_text="Number of rooms in the apartment. 11 if 10+ rooms.",
    )
    area = models.DecimalField(
        verbose_name=_("Area"), max_digits=8, decimal_places=2, blank=True, null=True
    )
    floor = models.CharField(
        verbose_name=_("Floor"),
        max_length=20,
        choices=FloorChoice.choices,
        blank=True,
        null=True,
    )  # floor is also in details, because here is string from the list
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=20,
        choices=ApartmentStatus.choices,
        blank=False,
        null=False,
        default=ApartmentStatus.WAITING_FOR_DETAILS,
    )
    lastly_scraped_at = (
        models.DateTimeField(auto_now_add=True, blank=True, null=True),
    )
    estimated_price = models.DecimalField(
        verbose_name=_("Estimated Price"),
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Apartment")
        verbose_name_plural = _("Apartments")

    @property
    def subpage_abs_path(self) -> URL:
        return URL(OTODOM_BASE_URL + self.subpage)

    @property
    def address_estate(self) -> str | None:
        with suppress(IndexError):
            return str(self.address).replace(" ", "").split(",")[-3]
        return None

    @property
    def price_per_m2(self) -> float | None:
        if self.price and self.area:
            return float(self.price) / float(self.area)
        return None

    @property
    def below_market_price(self) -> float | None:
        if self.price and self.estimated_price:
            return float(self.estimated_price) - float(self.price)
        return None

    def is_special_offer(self, treshold: float) -> bool:
        if self.below_market_price and treshold:
            return self.below_market_price > treshold
        return False

    def __str__(self):
        return f"Apartment(title={self.title[:20]}, price={self.price})"


class ApartmentDetails(BaseModel):
    apartment = models.OneToOneField(
        Apartment,
        verbose_name=_("Apartment"),
        related_name="details",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    exact_floor = models.PositiveSmallIntegerField(
        verbose_name=_("Real Floor"), blank=True, null=True
    )
    exact_rooms = models.PositiveSmallIntegerField(
        verbose_name=_("Real Rooms"), blank=True, null=True
    )
    max_floor = models.PositiveSmallIntegerField(
        verbose_name=_("Max Floor"), blank=True, null=True
    )
    rent = models.PositiveSmallIntegerField(
        verbose_name=_("Rent"), blank=True, null=True
    )
    energy_certificate = models.CharField(
        verbose_name=_("Energy Certificate"), max_length=64, blank=True, null=True
    )
    form_of_the_property = models.CharField(
        verbose_name=_("Form Of The Property"), max_length=64, blank=True, null=True
    )
    finishing_condition = models.CharField(
        verbose_name=_("Finishing Condition"),
        max_length=64,
        choices=FinishingConditionChoice.choices,
        blank=True,
        null=True,
    )
    balcony_garden_terrace = models.CharField(
        verbose_name=_("Balcony Garden"), max_length=64, blank=True, null=True
    )
    parking_place = models.CharField(
        verbose_name=_("Parking Place"), max_length=64, blank=True, null=True
    )
    heating = models.CharField(
        verbose_name=_("Heating"), max_length=64, blank=True, null=True
    )
    description = models.TextField(
        verbose_name=_("Full Description"), blank=True, null=True
    )
    market = models.CharField(
        verbose_name=_("Market"),
        max_length=64,
        choices=MarketChoice.choices,
        blank=True,
        null=True,
    )
    advertisement_type = models.CharField(
        verbose_name=_("Advertisement Type"), max_length=128, blank=True, null=True
    )
    year_of_construction = models.PositiveSmallIntegerField(
        verbose_name=_("Year of Construction"), blank=True, null=True
    )
    type_of_development = models.CharField(
        verbose_name=_("Type of Development"), max_length=64, blank=True, null=True
    )
    windows = models.CharField(
        verbose_name=_("Windows"), max_length=128, blank=True, null=True
    )
    is_elevator = models.BooleanField(
        verbose_name=_("Is Elevator"), blank=True, null=True
    )

    class Meta:
        verbose_name = _("Apartment Details")
        verbose_name_plural = _("Apartments Details")

    def __str__(self):
        return f"{self.apartment} - details"

    @property
    def a_title(self):
        return self.apartment.title

    @property
    def a_id(self):
        return self.apartment.id

    @property
    def a_price(self):
        return self.apartment.price

    @property
    def a_estimated_price(self):
        return self.apartment.estimated_price
