# Generated by Django 2.2.9 on 2020-04-07 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djpmp', '0012_staff_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hrcalendar',
            name='ev',
            field=models.FloatField(choices=[(0, 0), (0.5, 0.5), (1, 1), (1.5, 1.5), (2, 2)], default=0),
        ),
    ]
