# Generated by Django 3.1.7 on 2021-04-01 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='parts_worked',
            field=models.JSONField(default=[]),
            preserve_default=False,
        ),
    ]
