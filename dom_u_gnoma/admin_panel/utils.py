from django.shortcuts import redirect

from orders.models import Order


def change_flag(order, attr, msg=None):
    """Меняет значение payed или checked заказа на противоположное.

    Args:
        order (Order): обьект заказа.
        attr (str): имя атрибута для замены.
        msg (bool, optional): флаг для страницы с формой сообщения.
        По умолчанию - None.

    Если функция вызвана из view для страницы с формой сообщения:
        Меняет значение payed или checked заказа на противоположное.
    Иначе:
        Returns:
            HttpResponseRedirect: перенаправляет на страницу панели
            администратора с заказами.
    """

    if not msg:
        setattr(order, attr, abs(getattr(order, attr) - 1))
        order.save(update_fields=[attr])
        return redirect('admin_panel:orders')
    setattr(order, attr, True)
    order.save(update_fields=[attr])


def add_count_to_context(context):
    """Добавляет в контекст счетчик не обработанных заказов.

    Args:
        context (dict): контекст.

    Returns:
        dict: контекст.
    """

    context.update({
        'count': Order.objects.filter(checked=False).count()
    })
    return context
