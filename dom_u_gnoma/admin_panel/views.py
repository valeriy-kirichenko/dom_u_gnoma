from typing import Any, Dict

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Prefetch, Sum
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import OrderMessageForm
from .utils import add_count_to_context, change_flag
from items.models import Item
from orders.models import Order


def is_admin(user):
    return user.is_superuser


class AdminOrdersView(UserPassesTestMixin, TemplateView):
    template_name = 'admin_panel/admin_orders.html'

    def handle_no_permission(self):
        return redirect('about:index')

    def test_func(self):
        return is_admin(self.request.user)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        prefetch = Prefetch(
            'items', queryset=Item.objects.all().only('name', 'price')
        )
        orders = Order.objects.all().prefetch_related(prefetch).annotate(
            total=Sum('items__price')
        )
        context.update({
            'orders': orders,
            'count': orders.filter(checked=False).count()
        })
        return context


class AdminMenuView(UserPassesTestMixin, TemplateView):
    template_name = 'admin_panel/admin_menu.html'

    def handle_no_permission(self):
        return redirect('about:index')

    def test_func(self):
        return is_admin(self.request.user)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return add_count_to_context(context)


class AdminOrderMessageView(UserPassesTestMixin, CreateView):
    form_class = OrderMessageForm
    template_name = 'admin_panel/admin_order_message.html'
    success_url = reverse_lazy('admin_panel:orders')

    def test_func(self):
        return is_admin(self.request.user)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return add_count_to_context(context)

    def form_valid(self, form: ModelForm) -> HttpResponse:
        message = form.save(commit=False)
        message.user = self.request.user
        order = Order.objects.get(id=self.kwargs['id'])
        message.order = order
        change_flag(order, 'checked', msg=True)
        return super().form_valid(form)


@user_passes_test(is_admin, login_url='/')
def admin_check_order(request, id):
    return change_flag(get_object_or_404(Order, id=id), 'checked')


@user_passes_test(is_admin, login_url='/')
def admin_order_delete(request, id):
    order = get_object_or_404(Order, id=id)
    for item in order.items.all():
        item.is_published = True
        item.save(update_fields=['is_published'])
    order.delete()
    return redirect('admin_panel:orders')


@user_passes_test(is_admin, login_url='/')
def admin_order_payed(request, id):
    return change_flag(get_object_or_404(Order, id=id), 'payed')
