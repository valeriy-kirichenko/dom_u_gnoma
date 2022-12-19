from cart.models import Cart
from cart.utils import get_cart_items


def get_and_add_items_to_order(order, user):
    cart = Cart.objects.filter(user=user.id)
    items = get_cart_items(user)
    for item in items:
        item.is_published = False
        item.order = order
        item.save()
    cart.delete()


def add_user_to_order(order, user):
    order.user = user
    order.save()
    get_and_add_items_to_order(order, user)
