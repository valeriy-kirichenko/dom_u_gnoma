from django.conf import settings
from django.shortcuts import get_object_or_404, render

from .models import Item
from .utils import get_and_update_session
from cart.models import Cart


def catalog(request):
    """View-функция для отображения изделий в аталоге.

    Args:
        request (HttpRequest): обьект запроса.

    Returns:
        HttpResponse: обьект ответа, страница каталога.
    """

    items = Item.objects.filter(
        is_published=True
    ).values('id', 'name', 'image')
    context = {'items': items}
    return render(request, 'items/catalog.html', context)


def item_detail(request, id):
    """View-функция для отображения страницы изделия.

    Args:
        request (HttpRequest): обьект запроса.
        id (int): id изделия.

    Returns:
        HttpResponse: обьект ответа, страница изделия.
    """

    session = get_and_update_session(request)
    item = get_object_or_404(
        Item.objects.values(
            'id', 'name', 'image', 'description', 'price'
        ),
        id=id
    )
    # Проверяем находится ли изделие в корзине анонимного/залогиненного
    # пользователя что бы передать в контекст переменную added.
    if (
        session.get(settings.SESSION_CART) and
        str(id) in session[settings.SESSION_CART].keys() or
        Cart.objects.filter(user=request.user.id, item=id).exists()
    ):
        added = True
    else:
        added = False
    context = {'item': item, 'added': added}
    return render(request, 'items/item_detail.html', context)
