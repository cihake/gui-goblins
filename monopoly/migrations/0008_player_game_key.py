# Generated by Django 5.0.3 on 2024-04-12 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0007_remove_player_game_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='game_key',
            field=models.UUIDField(null=True, unique=True),
        ),
    ]
