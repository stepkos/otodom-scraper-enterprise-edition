# Generated by Django 5.0.6 on 2024-06-19 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scrapers", "0005_alter_scrapersession_treshold"),
    ]

    operations = [
        migrations.AddField(
            model_name="scrapersession",
            name="artificial_page_stop",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]