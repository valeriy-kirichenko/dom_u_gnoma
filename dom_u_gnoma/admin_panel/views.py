from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Prefetch, Sum
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
    """View-класс для отображения меню панели администратора."""

    template_name = 'admin_panel/admin_orders.html'

    def handle_no_permission(self):
        """Перенаправляет пользователя у которого нет прав для просмотра
        страницы.

        Returns:
            HttpResponseRedirect: перенаправляет на главную страницу.
        """

        return redirect('about:index')

    def test_func(self):
        """Проверяет статус пользователя.

        Returns:
            bool: True если администратор иначе False.
        """

        return is_admin(self.request.user)

    def get_context_data(self, **kwargs):
        """Добавляет в контекст заказы и счетчик не проверенных заказов.

        Returns:
            dict: контекст.
        """

        context = super().get_context_data(**kwargs)
        # Сперва уточняем какие именно поля взять у изделий.
        prefetch = Prefetch(
            'items', queryset=Item.objects.all().only('name', 'price')
        )
        # Получем заказы и связанные с ними изделия а так же добавляем общую
        # стоймость изделий в заказе.
        orders = Order.objects.all().prefetch_related(prefetch).annotate(
            total=Sum('items__price')
        )
        context.update({
            'orders': orders,
            'count': orders.filter(checked=False).count()
        })
        return context


class AdminMenuView(UserPassesTestMixin, TemplateView):
    """View-класс для отображения меню панели администратора."""

    template_name = 'admin_panel/admin_menu.html'

    def handle_no_permission(self):
        """Перенаправляет пользователя у которого нет прав для просмотра
        страницы.

        Returns:
            HttpResponseRedirect: перенаправляет на главную страницу.
        """

        return redirect('about:index')

    def test_func(self):
        """Проверяет статус пользователя.

        Returns:
            bool: True если администратор иначе False.
        """

        return is_admin(self.request.user)

    def get_context_data(self, **kwargs):
        """Добавляет в контекст счетчик необработанных заказов.

        Returns:
            dict: контекст.
        """

        context = super().get_context_data(**kwargs)
        return add_count_to_context(context)


class AdminOrderMessageView(UserPassesTestMixin, CreateView):
    """View-класс для отображения формы отправки сообщения с инструкциями по
    оплате заказа.
    """

    form_class = OrderMessageForm
    template_name = 'admin_panel/admin_order_message.html'
    success_url = reverse_lazy('admin_panel:orders')

    def test_func(self):
        """Проверяет статус пользователя.

        Returns:
            bool: True если администратор иначе False.
        """

        return is_admin(self.request.user)

    def get_context_data(self, **kwargs):
        """Добавляет в контекст счетчик необработанных заказов.

        Returns:
            dict: контекст.
        """

        context = super().get_context_data(**kwargs)
        return add_count_to_context(context)

    def form_valid(self, form):
        """После проверки формы добавляет к сообщению пользователя и заказ,
        так же меняет у заказа статус на "Обработан".

        Args:
            form (OrderMessageForm): обьект формы сообщения.

        Returns:
            HttpResponseRedirect: перенаправляет на страницу панели
            администратора с заказами.
        """

        message = form.save(commit=False)
        message.user = self.request.user
        order = Order.objects.get(id=self.kwargs['id'])
        message.order = order
        change_flag(order, 'checked', msg=True)
        return super().form_valid(form)


@user_passes_test(is_admin)
def admin_check_order(request, id):
    """View-функция для изменения у заказа статуса на "Обработан".

    Args:
        request (HttpRequest): обьект запроса.
        id (int): id заказа.

    Returns:
        HttpResponseRedirect: перенаправляет на страницу панели
            администратора с заказами.
    """

    return change_flag(get_object_or_404(Order, id=id), 'checked')


@user_passes_test(is_admin)
def admin_order_delete(request, id):
    """View-функция для удаления заказа и возвращения изделий из него в
    каталог изделий.

    Args:
        request (HttpRequest): обьект запроса.
        id (int): id заказа.

    Returns:
        HttpResponseRedirect: перенаправляет на страницу панели
            администратора с заказами.
    """

    order = get_object_or_404(Order, id=id)
    for item in order.items.all():
        item.is_published = True
        item.save(update_fields=['is_published'])
    order.delete()
    return redirect('admin_panel:orders')


@user_passes_test(is_admin)
def admin_order_payed(request, id):
    """View-функция для изменения у заказа статуса на "Оплачен".

    Args:
        request (HttpRequest): обьект запроса.
        id (int): id заказа.

    Returns:
        HttpResponseRedirect: перенаправляет на страницу панели
            администратора с заказами.
    """

    return change_flag(get_object_or_404(Order, id=id), 'payed')
