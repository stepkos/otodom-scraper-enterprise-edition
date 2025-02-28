# Generated by Django 5.0.6 on 2024-06-17 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartments", "0007_apartment_was_deleted"),
    ]

    operations = [
        migrations.AddField(
            model_name="apartment",
            name="status",
            field=models.CharField(
                choices=[
                    ("WAITING_FOR_DETAILS", "Awaiting details"),
                    ("SYNCHRONIZED", "Synchronized"),
                    ("DELETED", "deleted"),
                ],
                default="WAITING_FOR_DETAILS",
                max_length=20,
                verbose_name="Status",
            ),
        ),
        migrations.AddField(
            model_name="apartmentdetails",
            name="exact_floor",
            field=models.PositiveSmallIntegerField(
                blank=True, null=True, verbose_name="Real Floor"
            ),
        ),
        migrations.AddField(
            model_name="apartmentdetails",
            name="exact_rooms",
            field=models.PositiveSmallIntegerField(
                blank=True, null=True, verbose_name="Real Rooms"
            ),
        ),
        migrations.AlterField(
            model_name="apartment",
            name="rooms",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text="Number of rooms in the apartment. 11 if 10+ rooms.",
                null=True,
                verbose_name="Rooms",
            ),
        ),
    ]
