# Generated by Django 5.0.3 on 2024-04-12 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catan', '0007_alter_game_number_players_alter_game_turn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='number_players',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='game',
            name='turn',
            field=models.IntegerField(default=1),
        ),
    ]
