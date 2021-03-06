# Generated by Django 3.2.8 on 2021-10-11 09:03

from api.models import AllowCountry
from django.db import migrations


def insert_first_peak(apps, schema_editor):
    insertion = AllowCountry(
        name="France",
        code="FR"
    )
    insertion.save()


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0008_allowcountry'),
    ]

    operations = [
        migrations.RunPython(insert_first_peak),
    ]
