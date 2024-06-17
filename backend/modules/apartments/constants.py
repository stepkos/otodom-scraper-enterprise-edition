from django.db import models
from django.utils.translation import gettext_lazy as _


class FloorChoice(models.TextChoices):
    ATTIC = "poddasze", _("Attic")
    BASEMENT = "suterena", _("Basecment")
    GROUND_FLOOR = "parter", _("Ground floor")
    UPPER_THAN_TENTH = "10+", _("Upper than 10")
    FIRST = "1", "1"
    SECOND = "2", "2"
    THIRD = "3", "3"
    FOURTH = "4", "4"
    FIFTH = "5", "5"
    SIXTH = "6", "6"
    SEVENTH = "7", "7"
    EIGHTH = "8", "8"
    NINTH = "9", "9"
    TENTH = "10", "10"


class ApartmentStatus(models.TextChoices):
    WAITING_FOR_DETAILS = "WAITING_FOR_DETAILS", _("Awaiting details")
    SYNCHRONIZED = "SYNCHRONIZED", _("Synchronized")
    DELETED = "DELETED", _("deleted")
