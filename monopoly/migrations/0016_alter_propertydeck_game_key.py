# Generated by Django 5.0.3 on 2024-04-16 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0015_alter_propertydeck_game_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertydeck',
            name='game_key',
            field=models.UUIDField(null=True, unique=True),
        ),
    ]
