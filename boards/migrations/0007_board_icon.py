# Generated by Django 3.2.5 on 2021-08-19 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0006_auto_20210318_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='icon',
            field=models.CharField(default='💼', max_length=2),
        ),
    ]
