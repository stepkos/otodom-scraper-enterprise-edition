# Generated by Django 5.0.6 on 2024-06-19 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartments", "0010_alter_apartmentdetails_finishing_condition_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="apartment",
            name="estimated_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=0,
                max_digits=10,
                null=True,
                verbose_name="Estimated Price",
            ),
        ),
    ]
