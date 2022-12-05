from django.core.signing import Signer
from django.template.loader import render_to_string
from django.conf import settings

from cart.models import Cart
from cart.utils import get_session_cart
from items.models import Item


signer = Signer()


def send_activation_notification(user):
    if settings.ALLOWED_HOSTS:
        host = 'http://' + settings.ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)


def check_anonymous_cart(request, user):
    session = request.session
    anonymous_cart = get_session_cart(session)
    user_cart = Cart.objects.filter(
        user_id=user.id
    ).values_list('item', flat=True)
    ids_to_add = [
        int(id) for id in anonymous_cart.keys() if int(id) not in user_cart
    ]
    if ids_to_add:
        Cart.objects.bulk_create(
            Cart(
                user=user,
                item=Item.objects.get(id=pk)
                ) for pk in ids_to_add
        )
        anonymous_cart.clear()


def user_logged_in_dispatcher(sender, **kwargs):
    check_anonymous_cart(kwargs['request'], kwargs['user'])


def user_registered_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])
