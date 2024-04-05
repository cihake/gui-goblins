# Generated by Django 5.0.3 on 2024-04-05 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Corner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yindex', models.IntegerField()),
                ('xindex', models.IntegerField()),
                ('building', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_players', models.IntegerField()),
                ('turn', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yindex', models.IntegerField()),
                ('xindex', models.IntegerField()),
                ('terrain', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corners', models.ManyToManyField(related_name='board', to='catan.corner')),
                ('tiles', models.ManyToManyField(related_name='board', to='catan.tile')),
            ],
        ),
    ]
