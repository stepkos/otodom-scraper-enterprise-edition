# Generated by Django 5.0.6 on 2024-06-01 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartments", "0005_alter_apartment_address_alter_apartment_area_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apartmentdetails",
            name="energy_certificate",
            field=models.CharField(
                blank=True, max_length=64, null=True, verbose_name="Energy Certificate"
            ),
        ),
        migrations.AlterField(
            model_name="apartmentdetails",
            name="finishing_condition",
            field=models.CharField(
                blank=True, max_length=64, null=True, verbose_name="Finishing Condition"
            ),
        ),
        migrations.AlterField(
            model_name="apartmentdetails",
            name="form_of_the_property",
            field=models.CharField(
                blank=True,
                max_length=64,
                null=True,
                verbose_name="Form Of The Property",
            ),
        ),
        migrations.AlterField(
            model_name="apartmentdetails",
            name="market",
            field=models.CharField(
                blank=True, max_length=64, null=True, verbose_name="Market"
            ),
        ),
    ]
