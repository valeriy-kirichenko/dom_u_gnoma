from django.contrib import admin

from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item',)
    search_fields = ('user',)
    list_filter = ('user',)
