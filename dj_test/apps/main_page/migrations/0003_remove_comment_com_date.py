# Generated by Django 3.0.3 on 2020-02-20 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0002_auto_20200220_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='com_date',
        ),
    ]
