# Generated by Django 3.0.5 on 2020-06-02 21:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0006_auto_20200602_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author_name',
            field=models.CharField(default='Anonymous', max_length=50, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 2, 21, 49, 3, 899514, tzinfo=utc), verbose_name='Время публикации'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 2, 21, 49, 3, 899914, tzinfo=utc), verbose_name='Время публикации'),
        ),
    ]