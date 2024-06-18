from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ScrapersConfig(AppConfig):
    name = "modules.scrapers"
    verbose_name = _("Scrapers")
