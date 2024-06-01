from django.db import models
from django.utils.translation import gettext_lazy as _

from modules.core.models import BaseModel
from modules.scraper.constants.for_models import ScrapeStatusChoice


# class Url(BaseModel):
#     ...


class ScrapeRecord(BaseModel):
    url = models.URLField(verbose_name=_("URL"), unique=True)
    status = models.CharField(
        verbose_name=_("Status"), max_length=20, choices=ScrapeStatusChoice.choices
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == ScrapeStatusChoice.SCRAPE:
            # scrape_apartments.delay(self.id)
            pass
