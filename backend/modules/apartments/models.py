from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.apartments.constants import FloorChoice
from modules.core.models import BaseModel


class Apartment(BaseModel):
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    address = models.CharField(verbose_name=_("Address"), max_length=255)
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=10, decimal_places=0, blank=True, null=True
    )
    subpage = models.URLField(verbose_name=_("Subpage"), unique=True, editable=False)
    rooms = models.PositiveSmallIntegerField(verbose_name=_("Rooms"))
    area = models.DecimalField(verbose_name=_("Area"), max_digits=8, decimal_places=2)
    floor = models.CharField(
        verbose_name=_("Floor"), max_length=20, choices=FloorChoice.choices
    )

    class Meta:
        verbose_name = _("Apartment")
        verbose_name_plural = _("Apartments")

    # @property
    # def price_per_m2(self) -> Decimal | None:
    #     if self.price and self.area:
    #         return self.price / self.area
    #     return None

    def __str__(self):
        return f"Apartment(title={self.title[:20]}, price={self.price})"
