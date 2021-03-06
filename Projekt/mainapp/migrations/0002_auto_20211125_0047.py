# Generated by Django 3.2.8 on 2021-11-25 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mark',
            name='idSubjectStudent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.subjectstudent'),
        ),
        migrations.AlterField(
            model_name='student',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.school'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='teacherId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.teacher'),
        ),
        migrations.AlterField(
            model_name='subjectstudent',
            name='studentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.student'),
        ),
        migrations.AlterField(
            model_name='subjectstudent',
            name='subjectId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.subject'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.school'),
        ),
    ]
