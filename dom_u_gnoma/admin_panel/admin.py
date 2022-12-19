from django.contrib import admin

from .models import OrderMessage


@admin.register(OrderMessage)
class OrderMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order', 'text')
    search_fields = ('user',)
    list_filter = ('user',)
