# Generated by Django 3.1.4 on 2021-03-18 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0005_auto_20201223_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='boards.board'),
        ),
    ]
