from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ScraperConfig(AppConfig):
    name = "modules.scraper"
    verbose_name = _("Scraper")
