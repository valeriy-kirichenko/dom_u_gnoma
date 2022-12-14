# Generated by Django 4.1.3 on 2022-11-30 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_cart'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('-id',), 'verbose_name': 'Изделие', 'verbose_name_plural': 'Изделия'},
        ),
        migrations.AddField(
            model_name='item',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Опубликовано'),
        ),
    ]
