# Generated by Django 4.1.3 on 2022-12-16 11:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 16, 14, 37, 51, 262354), verbose_name='Дата создания'),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
