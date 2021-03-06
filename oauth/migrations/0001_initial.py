# Generated by Django 3.1.7 on 2021-03-19 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signup_date', models.DateField(verbose_name='User signup date')),
                ('bio', models.CharField(max_length=200, verbose_name='User Bio')),
                ('height', models.PositiveSmallIntegerField(blank=True, verbose_name='Height in inches')),
                ('weight', models.PositiveSmallIntegerField(blank=True, verbose_name='Weight in pounds')),
                ('points', models.PositiveIntegerField(verbose_name='Total accumulated points')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
