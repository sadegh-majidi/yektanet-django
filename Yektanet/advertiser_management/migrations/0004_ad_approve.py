# Generated by Django 2.2.17 on 2021-01-26 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0003_auto_20210126_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='approve',
            field=models.BooleanField(default=False, verbose_name='Approved'),
        ),
    ]
