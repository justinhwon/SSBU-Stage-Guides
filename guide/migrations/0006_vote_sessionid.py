# Generated by Django 3.0.7 on 2020-10-10 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0005_auto_20201003_0606'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='sessionid',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
