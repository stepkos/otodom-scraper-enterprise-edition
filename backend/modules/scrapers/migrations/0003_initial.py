# Generated by Django 5.0.6 on 2024-06-19 03:23

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("apartments", "0011_apartment_estimated_price"),
        ("scrapers", "0002_delete_scraperecord"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScraperSession",
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
                ("url", models.CharField(max_length=255)),
                (
                    "apartments",
                    models.ManyToManyField(
                        related_name="scraper_sessions", to="apartments.apartment"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
