# Generated by Django 4.1.3 on 2022-11-11 16:33

import django.core.validators
from django.db import migrations, models
import items.utils


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to=items.utils.image_directory_path, verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='item',
            name='weight',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0, 'Вес не может быть отрицательным')], verbose_name='Вес(гр)'),
        ),
    ]
