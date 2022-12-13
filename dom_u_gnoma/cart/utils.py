from django.conf import settings

from cart.models import Cart
from items.models import Item


def get_session_cart(session):
    if session.get(settings.SESSION_CART) is None:
        session[settings.SESSION_CART] = {}
    return session[settings.SESSION_CART]


def get_cart_items(user, session):
    if user.is_authenticated:
        ids = Cart.objects.filter(user=user.id).values_list('item', flat=True)
    else:
        ids = session[settings.SESSION_CART].keys()
    return Item.objects.filter(id__in=ids)


def add_delete_from_cart(request, id, add=True):
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
