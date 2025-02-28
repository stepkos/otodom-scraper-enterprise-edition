# Generated by Django 5.0.6 on 2024-05-31 23:11

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ScrapeRecord",
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
                ("url", models.URLField(unique=True, verbose_name="URL")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("scrape", "Scrape"),
                            ("in_progress", "In progress"),
                            ("done", "Done"),
                            ("error", "Error"),
                        ],
                        max_length=20,
                        verbose_name="Status",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
