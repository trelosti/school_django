# Generated by Django 4.2.2 on 2023-06-26 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='group',
            field=models.CharField(default='1-A', max_length=10, verbose_name='class'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='phone_number',
            field=models.CharField(default='0', max_length=20, verbose_name='phone_number'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='subject_name',
            field=models.CharField(default='none', max_length=255, verbose_name='subject_name'),
        ),
    ]
