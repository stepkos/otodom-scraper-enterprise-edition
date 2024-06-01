from django.db import models
from django.utils.translation import gettext_lazy as _


class ScrapeStatusChoice(models.TextChoices):
    SCRAPE = "scrape", _("Scrape")
    IN_PROGRESS = "in_progress", _("In progress")
    DONE = "done", _("Done")
    ERROR = "error", _("Error")
