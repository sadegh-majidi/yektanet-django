# Generated by Django 2.2.17 on 2021-01-26 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0002_auto_20210124_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='clicks',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='views',
        ),
        migrations.RemoveField(
            model_name='advertiser',
            name='clicks',
        ),
        migrations.RemoveField(
            model_name='advertiser',
            name='views',
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('click_time', models.DateTimeField(auto_now_add=True, verbose_name='Time')),
                ('user_ip', models.GenericIPAddressField(verbose_name='User IP')),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='advertiser_management.Ad', verbose_name='Viewed Ad')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Click',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('click_time', models.DateTimeField(auto_now_add=True, verbose_name='Time')),
                ('user_ip', models.GenericIPAddressField(verbose_name='User IP')),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clicks', to='advertiser_management.Ad', verbose_name='Clicked Ad')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]