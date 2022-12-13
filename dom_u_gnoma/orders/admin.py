from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'city',
        'phone',
        'email',
        'payed'
    )
    search_fields = ('id', 'user',)
    list_filter = ('id', 'user',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item',)
    search_fields = ('order', 'item',)
    list_filter = ('order',)
