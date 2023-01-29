from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy

from .forms import OrderCreationForm
from .models import Order
from .utils import add_user_to_order, get_and_add_items_to_order
from cart.utils import get_cart_items


class OrderCreateView(LoginRequiredMixin, CreateView):
    """View-класс для создания заказа."""

    form_class = OrderCreationForm
    success_url = reverse_lazy('orders:order_done')
    template_name = 'orders/order_create.html'

    def get_context_data(self, **kwargs):
        """Добавляет в контекст изделия и их общую стоимость.

        Returns:
            dict: контекст.
        """

        context = super().get_context_data(**kwargs)
        items = get_cart_items(self.request.user)
        total_price = items.aggregate(total_price=Sum('price'))
        context['items'] = items.values('name', 'price')
        context['total_price'] = "{:.2f}".format(total_price['total_price'])
        return context

    def form_valid(self, form):
        """Проверяет существующие заказы у пользователя, если их нет то
        добавляет товары в новый, если есть, проверяет статус последнего
        существующего заказа, если статус "Проверен" то добавляет товары в
        новый заказ, если статус "Не проверен" то добавляет товары с вновь
        создаваемого заказа в него.

        Args:
            form (OrderCreationForm): обьект формы заказа.

        Returns:
            HttpResponseRedirect: перенаправляет на страницу завершения
            оформления заказа.
        """

        order = form.save(commit=False)
        user = self.request.user
        try:
            # Проверяем есть ли у пользователя заказ(ы).
            existing_order = Order.objects.get(
                user=user,
                city=order.city,
                street=order.street,
                house=order.house,
                postal_code=order.postal_code
            )
        except Order.MultipleObjectsReturned:
            # Если у пользователя несколько заказов, берем последний созданный.
            existing_order = Order.objects.filter(
                user=user,
                city=order.city,
                street=order.street,
                house=order.house,
                postal_code=order.postal_code
            ).order_by('-created').first()
            if existing_order.checked:
                # Если последний созданный заказ проверен то создаем новый.
                add_user_to_order(order, user)
                return super().form_valid(form)
        except Order.DoesNotExist:
            # Если у пользователя отсутствуют заказы то создаем новый.
            add_user_to_order(order, user)
            return super().form_valid(form)
        if existing_order.checked:
            # Если последний созданный заказ проверен то создаем новый.
            add_user_to_order(order, user)
            return super().form_valid(form)
        # Если последний созданный заказ не проверен то добавляем в него
        # товары.
        get_and_add_items_to_order(existing_order, user)
        self.object = existing_order
        return redirect(self.get_success_url())


class OrderDoneView(TemplateView):
    """View-класс для вывода страницы завершения оформления заказа."""

    template_name = 'orders/order_done.html'
