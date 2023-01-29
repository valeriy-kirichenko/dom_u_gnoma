from django.core.signing import Signer
from django.template.loader import render_to_string
from django.conf import settings

from cart.models import Cart
from cart.utils import get_session_cart
from items.models import Item

signer = Signer()


def send_activation_notification(user):
    """Отправляет письмо с указаниями по активации пользователя.

    Args:
        user (User): обьект пользователя.
    """

    if settings.ALLOWED_HOSTS:
        host = 'http://' + settings.ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    # Так же передаем в контекст имя пользователя, защещенное цифровой
    # подписью.
    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)


def check_anonymous_cart(request, user):
    """Проверяет корзину анонимного пользователя на наличие изделий. Если
    изделия есть,то после аутентификации переносит их в корзину залогиненного
    пользователя и очищает корзину анонимного.

    Args:
        request (HttpRequest): обьект запроса.
        user (User): обьект пользователя.
    """

    session = request.session
    # Получаем корзину анонимного пользователя.
    anonymous_cart = get_session_cart(session)
    # Получаем id изделий из корзины залогиненного пользователя.
    user_cart_items_ids = Cart.objects.filter(
        user_id=user.id
    ).values_list('item', flat=True)
    # Определяем id изделий которых еще нету в корзине залогиненного
    # пользователя.
    ids_to_add = [
        int(id) for id in anonymous_cart.keys()
        if int(id) not in user_cart_items_ids
    ]
    # И если такие изделия присутствуют, добавляем их в корзину залогиненного
    # пользователя.
    if ids_to_add:
        Cart.objects.bulk_create(
            Cart(
                user=user,
                item=Item.objects.get(id=pk)
                ) for pk in ids_to_add
        )
        anonymous_cart.clear()


def user_logged_in_dispatcher(sender, **kwargs):
    """Диспетчер сигнала user_logged_in.

    Args:
        sender (Any): отправитель сигнала.
    """

    check_anonymous_cart(kwargs['request'], kwargs['user'])


def user_registered_dispatcher(sender, **kwargs):
    """Диспетчер сигнала user_registered.

    Args:
        sender (Any): отправитель сигнала.
    """

    send_activation_notification(kwargs['instance'])
