# Generated by Django 5.0.3 on 2024-04-16 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0013_rename_title_property_name_remove_player_properties_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertydeck',
            name='game_key',
            field=models.UUIDField(null=True, unique=True),
        ),
    ]
