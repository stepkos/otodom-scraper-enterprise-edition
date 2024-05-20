from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApartmentsConfig(AppConfig):
    name = "modules.apartments"
    verbose_name = _("Apartments")
