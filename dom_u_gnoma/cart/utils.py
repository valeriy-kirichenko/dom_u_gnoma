from django.conf import settings


def get_session_cart(session):
    if session.get(settings.SESSION_CART) is None:
        session[settings.SESSION_CART] = {}
    return session[settings.SESSION_CART]
