# Generated by Django 5.0.3 on 2024-04-08 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catan', '0003_game_turn'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='number_players',
            field=models.IntegerField(default=1),
        ),
    ]
