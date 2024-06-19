from django.db import models

from modules.apartments.models import Apartment
from modules.core.models import BaseModel


class ScraperSession(BaseModel):
    url = models.CharField(max_length=255)
    apartments = models.ManyToManyField(Apartment, related_name="scraper_sessions")
    treshold = models.DecimalField(
        verbose_name="Special offer treshold",
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    artificial_page_stop = models.IntegerField(null=True, blank=True)
