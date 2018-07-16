# Generated by Django 2.0 on 2018-07-15 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_server', '0002_auto_20180715_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citation_expansioin', models.BooleanField(default=False)),
                ('importance', models.IntegerField(default=0)),
                ('expansioin_depth', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='api_server.Article')),
            ],
        ),
        migrations.RemoveField(
            model_name='citation',
            name='citation_id',
        ),
        migrations.RemoveField(
            model_name='citation',
            name='cited_id',
        ),
        migrations.AddField(
            model_name='citation',
            name='cited',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='cited', to='api_server.Article'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='citation',
            name='citing',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='citing', to='api_server.Article'),
            preserve_default=False,
        ),
    ]