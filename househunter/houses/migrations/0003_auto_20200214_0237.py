# Generated by Django 3.0.3 on 2020-02-14 02:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0002_auto_20200214_0236'),
    ]

    operations = [
        migrations.RenameField(
            model_name='house',
            old_name='last_sold',
            new_name='last_sold_date',
        ),
    ]
