# Generated by Django 2.0 on 2018-07-16 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_server', '0005_auto_20180715_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='url_citations',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='article',
            name='url_versions',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]