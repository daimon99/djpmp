# Generated by Django 2.2.9 on 2020-04-02 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djpmp', '0009_auto_20200402_1742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='user',
        ),
    ]
