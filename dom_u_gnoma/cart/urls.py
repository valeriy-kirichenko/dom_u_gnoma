from django.urls import path

from . import views


app_name = 'cart'

urlpatterns = [
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('delete/<int:id>/', views.delete_from_cart, name='delete_from_cart'),
    path('items/', views.items, name='items'),
]
