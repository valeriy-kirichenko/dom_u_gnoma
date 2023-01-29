from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse

from .utils import add_delete_from_cart, get_cart_items, get_session_cart
from items.utils import get_and_update_session


def add_to_cart(request, id):
    """View-функция для добавления товара в корзину.

    Args:
        request (HttpRequest): обьект запроса.
        id (int): id изделияю

    Returns:
        HttpResponseRedirect: перенаправляет на страницу изделия.
    """

    add_delete_from_cart(request, id)
    return redirect('items:item_detail', id=id)


def delete_from_cart(request, id):
    """View-функция для удаления товара из корзины.

    Args:
        request (HttpRequest): обьект запроса.
        id (int): id изделияю

    Если пользователь находится в каталоге:
        Returns:
            HttpResponseRedirect: перенаправляет на страницу каталога.
    Иначе:
        Returns:
            HttpResponseRedirect: перенаправляет на текущую страницу.
    """

    add_delete_from_cart(request, id, add=False)
    if request.session['path'] == reverse('cart:items'):
        return redirect('cart:items')
    return redirect(request.session['path'])


def items(request):
    """View-функция для страницы корзины.

    Args:
        request (HttpRequest): обьект запроса.

    Returns:
        HttpResponse: обьект ответа, страница корзины.
    """

    session = get_and_update_session(request)
    get_session_cart(session)
    user = request.user
    items = get_cart_items(user, session)
    # Общая стоймость товаров в корзине
    total_amount = items.aggregate(total=Sum('price'))
    if total_amount['total'] is None:
        total_amount['total'] = 0
    context = {
        'items': items,
        'total_amount': "{:.2f}".format(total_amount['total'])
    }
    return render(request, 'cart/items.html', context)
