# Generated by Django 5.0.3 on 2024-05-06 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catan', '0021_remove_board_robberx_remove_board_robbery_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='cities',
            field=models.IntegerField(default=0),
        ),
    ]
