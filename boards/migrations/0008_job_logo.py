# Generated by Django 3.2.6 on 2021-08-30 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0007_board_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='logo',
            field=models.CharField(default='https://via.placeholder.com/130?text=Company+Logo', max_length=100),
        ),
    ]
