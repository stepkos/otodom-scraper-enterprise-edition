from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmailsConfig(AppConfig):
    name = "modules.emails"
    verbose_name = _("Emails")
