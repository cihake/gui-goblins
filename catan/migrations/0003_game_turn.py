# Generated by Django 5.0.3 on 2024-04-08 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catan', '0002_remove_game_number_players_remove_game_turn'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='turn',
            field=models.IntegerField(default=1),
        ),
    ]
