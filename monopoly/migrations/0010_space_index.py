# Generated by Django 5.0.3 on 2024-04-13 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0009_space_board'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='index',
            field=models.IntegerField(default=0),
        ),
    ]
