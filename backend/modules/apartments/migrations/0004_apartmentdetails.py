# Generated by Django 5.0.6 on 2024-05-31 23:11

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartments", "0003_alter_apartment_subpage"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApartmentDetails",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "max_floor",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Max Floor"
                    ),
                ),
                (
                    "rent",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Rent"
                    ),
                ),
                (
                    "energy_certificate",
                    models.CharField(
                        blank=True,
                        max_length=4,
                        null=True,
                        verbose_name="Energy Certificate",
                    ),
                ),
                (
                    "form_of_the_property",
                    models.CharField(
                        blank=True,
                        max_length=32,
                        null=True,
                        verbose_name="Form Of The Property",
                    ),
                ),
                (
                    "finishing_condition",
                    models.CharField(
                        blank=True,
                        max_length=32,
                        null=True,
                        verbose_name="Finishing Condition",
                    ),
                ),
                (
                    "balcony_garden_terrace",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        null=True,
                        verbose_name="Balcony Garden",
                    ),
                ),
                (
                    "parking_place",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        null=True,
                        verbose_name="Parking Place",
                    ),
                ),
                (
                    "heating",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="Heating"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Full Description"
                    ),
                ),
                (
                    "market",
                    models.CharField(
                        blank=True, max_length=32, null=True, verbose_name="Market"
                    ),
                ),
                (
                    "advertisement_type",
                    models.CharField(
                        blank=True,
                        max_length=128,
                        null=True,
                        verbose_name="Advertisement Type",
                    ),
                ),
                (
                    "year_of_construction",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Year of Construction"
                    ),
                ),
                (
                    "type_of_development",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        null=True,
                        verbose_name="Type of Development",
                    ),
                ),
                (
                    "windows",
                    models.CharField(
                        blank=True, max_length=128, null=True, verbose_name="Windows"
                    ),
                ),
                (
                    "is_elevator",
                    models.BooleanField(
                        blank=True, null=True, verbose_name="Is Elevator"
                    ),
                ),
                (
                    "apartment",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="details",
                        to="apartments.apartment",
                        verbose_name="Apartment",
                    ),
                ),
            ],
            options={
                "verbose_name": "Apartment Details",
                "verbose_name_plural": "Apartments Details",
            },
        ),
    ]
