# Generated by Django 4.1.3 on 2022-12-14 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='checked',
            field=models.BooleanField(default=False, verbose_name='Проверен'),
        ),
    ]
