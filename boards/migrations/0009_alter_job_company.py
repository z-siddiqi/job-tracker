# Generated by Django 3.2.6 on 2021-09-11 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0008_job_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.CharField(help_text="Logos provided by <a href='https://clearbit.com' target='_blank'>Clearbit</a>.", max_length=100),
        ),
    ]
