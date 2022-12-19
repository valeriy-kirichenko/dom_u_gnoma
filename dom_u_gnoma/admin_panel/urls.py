from django.urls import path

from . import views


app_name = 'admin_panel'

urlpatterns = [
    path(
        'orders/delete/<int:id>/',
        views.admin_order_delete,
        name='order_delete'
    ),
    path('orders/payed/<int:id>/', views.admin_order_payed, name='payed'),
    path('orders/checked/<int:id>/', views.admin_check_order, name='checked'),
    path(
        'orders/order-message/<int:id>/',
        views.AdminOrderMessageView.as_view(),
        name='order_message'
        ),
    path('menu/', views.AdminMenuView.as_view(), name='menu'),
    path('orders/', views.AdminOrdersView.as_view(), name='orders'),
]
