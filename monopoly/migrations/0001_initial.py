# Generated by Django 5.0.3 on 2024-04-10 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_key', models.UUIDField(unique=True)),
                ('winner', models.IntegerField(default=0)),
                ('turn', models.IntegerField(default=1)),
                ('number_players', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordinal', models.IntegerField(default=0)),
                ('space', models.IntegerField(default=0)),
                ('money', models.IntegerField(default=0)),
            ],
        ),
    ]
