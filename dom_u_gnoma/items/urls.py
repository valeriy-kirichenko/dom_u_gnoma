from django.urls import path

from . import views


app_name = 'items'

urlpatterns = [
    path('catalog/<int:id>/', views.item_detail, name='item_detail'),
    path('catalog/', views.catalog, name='catalog'),
]
