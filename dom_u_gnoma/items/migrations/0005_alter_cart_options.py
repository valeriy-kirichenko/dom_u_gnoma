# Generated by Django 4.1.3 on 2022-12-01 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_alter_item_options_item_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ('-id',), 'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзины'},
        ),
    ]
