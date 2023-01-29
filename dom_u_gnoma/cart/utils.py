from django.conf import settings

from cart.models import Cart
from items.models import Item


def get_session_cart(session):
    """Возвращет словарь с изделиями в корзине.

    Args:
        session (SessionStore): обьект сессии.

    Returns:
        dict: словарь с изделиями в корзине.
    """

    if session.get(settings.SESSION_CART) is None:
        session[settings.SESSION_CART] = {}
    return session[settings.SESSION_CART]


def get_cart_items(user, session=None):
    """Получает изделия из корзины залогиненого/анонимного пользователя.

    Args:
        user (User): обьект кользователя.
        session (SessionStore, optional): сессия. По умолчанию - None.

    Returns:
        QuerySet: изделия которые находятся в корзине.
    """

    if user.is_authenticated:
        # Получаем id изделий из корзины залогиненого пользователя.
        # <QuerySet [1, 2]>
        ids = Cart.objects.filter(user=user.id).values_list('item', flat=True)
    else:
        # Получаем id изделий из корзины анонимного пользователя.
        # <QuerySet [1, 2]>
        ids = session[settings.SESSION_CART].keys()
    return Item.objects.filter(id__in=ids)


def add_delete_from_cart(request, id, add=True):
    """Добавляет/удаляет товар из корзины.

    Args:
        request (HttpReques): обьект запроса.
        id (int): id изделия.
        add (bool, optional): флаг для добавления изделия. По умолчанию - True.
    """

    session = request.session
    get_session_cart(session)
    item = Item.objects.get(id=id)
    if request.user.is_authenticated:
        if not add:
            Cart.objects.get(user=request.user, item=item).delete()
        else:
            Cart.objects.create(user=request.user, item=item)
    else:
        if not add:
            del session[settings.SESSION_CART][str(id)]
        else:
            session[settings.SESSION_CART][str(id)] = 'В корзине'
        session.modified = True
