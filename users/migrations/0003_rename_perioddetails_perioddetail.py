# Generated by Django 5.0.3 on 2024-03-08 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_perioddetails'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PeriodDetails',
            new_name='PeriodDetail',
        ),
    ]