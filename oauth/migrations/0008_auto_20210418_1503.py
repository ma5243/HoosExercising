# Generated by Django 3.2 on 2021-04-18 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0007_profile_profile_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-points']},
        ),
        migrations.AddField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(null=True, related_name='_oauth_profile_friends_+', to='oauth.Profile', verbose_name='Friend list'),
        ),
    ]
