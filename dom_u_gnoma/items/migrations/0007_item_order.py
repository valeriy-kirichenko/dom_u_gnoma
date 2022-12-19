# Generated by Django 4.1.3 on 2022-12-16 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_created_delete_orderitem'),
        ('items', '0006_delete_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='orders.order', verbose_name='Заказ'),
        ),
    ]