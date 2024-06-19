from modules.apartments.models import Apartment
from modules.core.models import BaseModel
from django.db import models


class ScraperSession(BaseModel):
    url = models.CharField(max_length=255)
    apartments = models.ManyToManyField(Apartment, related_name='scraper_sessions')
    treshold = models.DecimalField(
        verbose_name="Occasion treshold", max_digits=10, decimal_places=0, blank=True, null=True
    )
