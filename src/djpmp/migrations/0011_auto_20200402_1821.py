# Generated by Django 2.2.9 on 2020-04-02 10:21

from django.db import migrations, models
import django.db.models.deletion
import djpmp.models


class Migration(migrations.Migration):

    dependencies = [
        ('djpmp', '0010_remove_project_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('未开始', '未开始'), ('进行中', '进行中'), ('完成', '完成')], default='进行中', max_length=64, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='hrcalendar',
            name='project',
            field=models.ForeignKey(limit_choices_to=djpmp.models.my_projects, on_delete=django.db.models.deletion.CASCADE, to='djpmp.Project', verbose_name='项目'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='project',
            field=models.ForeignKey(limit_choices_to=djpmp.models.my_projects, on_delete=django.db.models.deletion.CASCADE, to='djpmp.Project', verbose_name='项目'),
        ),
        migrations.AlterField(
            model_name='wbs',
            name='project',
            field=models.ForeignKey(limit_choices_to=djpmp.models.my_projects, on_delete=django.db.models.deletion.CASCADE, to='djpmp.Project', verbose_name='项目'),
        ),
    ]
