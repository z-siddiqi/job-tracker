# Generated by Django 3.1.4 on 2020-12-07 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boards', '0004_auto_20201207_1436'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, null=True, verbose_name='')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.job')),
            ],
        ),
    ]
