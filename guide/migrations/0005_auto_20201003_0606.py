# Generated by Django 3.0.7 on 2020-10-03 13:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0004_vote_small_battlefield'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='timestampCreated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vote',
            name='timestampUpdated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
    ]
