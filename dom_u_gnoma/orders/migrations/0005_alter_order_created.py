# Generated by Django 4.1.3 on 2022-12-19 13:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 19, 16, 2, 19, 798320), verbose_name='Дата создания'),
        ),
    ]
