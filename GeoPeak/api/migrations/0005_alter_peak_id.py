# Generated by Django 3.2.8 on 2021-10-10 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_peak_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peak',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
