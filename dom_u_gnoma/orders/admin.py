from django.contrib import admin

from .models import Order


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
