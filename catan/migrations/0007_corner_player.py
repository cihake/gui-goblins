# Generated by Django 5.0.3 on 2024-04-08 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catan', '0006_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='corner',
            name='player',
            field=models.IntegerField(default=1),
        ),
    ]
