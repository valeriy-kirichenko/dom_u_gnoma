from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy

from .forms import OrderCreationForm
from .models import Order
from .utils import add_user_to_order, get_and_add_items_to_order
from cart.utils import get_cart_items


class OrderCreateView(LoginRequiredMixin, CreateView):
    form_class = OrderCreationForm
    success_url = reverse_lazy('orders:order_done')
    template_name = 'orders/order_create.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        items = get_cart_items(self.request.user)
        total_price = items.aggregate(total_price=Sum('price'))
        context['items'] = items.values('name', 'price')
        context['total_price'] = "{:.2f}".format(total_price['total_price'])
        return context

    def form_valid(self, form: ModelForm) -> HttpResponse:
        order = form.save(commit=False)
        user = self.request.user
        try:
            existing_order = Order.objects.get(
                user=user,
                city=order.city,
                street=order.street,
                house=order.house,
                postal_code=order.postal_code
            )
        except Order.MultipleObjectsReturned:
            existing_order = Order.objects.filter(
                user=user,
                city=order.city,
                street=order.street,
                house=order.house,
                postal_code=order.postal_code
            ).order_by('-created').first()
            if existing_order.checked:
                add_user_to_order(order, user)
                return super().form_valid(form)
        except Order.DoesNotExist:
            add_user_to_order(order, user)
            return super().form_valid(form)
        if existing_order.checked:
            add_user_to_order(order, user)
            return super().form_valid(form)
        get_and_add_items_to_order(existing_order, user)
        self.object = existing_order
        return redirect(self.get_success_url())


class OrderDoneView(TemplateView):
    template_name = 'orders/order_done.html'
