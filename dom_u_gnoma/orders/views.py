from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.forms import ModelForm
from django.http import HttpResponse
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy

from .forms import OrderCreationForm
from .models import OrderItem
from cart.models import Cart
from cart.utils import get_cart_items


class OrderCreateView(LoginRequiredMixin, CreateView):
    form_class = OrderCreationForm
    success_url = reverse_lazy('orders:order_done')
    template_name = 'orders/order_create.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        items = get_cart_items(self.request.user, self.request.session)
        total_price = items.aggregate(total_price=Sum('price'))
        context['items'] = items.values('name', 'price')
        context['total_price'] = "{:.2f}".format(total_price['total_price'])
        return context

    def form_valid(self, form: ModelForm) -> HttpResponse:
        order = form.save(commit=False)
        user = self.request.user
        order.user = user
        order.save()
        cart = Cart.objects.filter(user=user.id)
        items = get_cart_items(user, self.request.session)
        for item in items:
            item.is_published = False
            item.save()
        OrderItem.objects.bulk_create(
            OrderItem(
                order=order,
                item=item
            ) for item in items
        )
        cart.delete()
        return super().form_valid(form)


class OrderDoneView(TemplateView):
    template_name = 'orders/order_done.html'
