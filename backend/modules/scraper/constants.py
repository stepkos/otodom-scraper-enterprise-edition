from django.db import models
from django.utils.translation import gettext_lazy as _


HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 '
                  'Safari/537.3'
}


class ScrapeStatusChoice(models.TextChoices):
    SCRAPE = "scrape", _("Scrape")
    IN_PROGRESS = "in_progress", _("In progress")
    DONE = "done", _("Done")
    ERROR = "error", _("Error")
