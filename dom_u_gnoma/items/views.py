from django.conf import settings
from django.shortcuts import get_object_or_404, render

from .models import Item
from cart.models import Cart


def catalog(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'items/catalog.html', context)


def item_detail(request, id):
    session = request.session
    session['path'] = request.path
    session.modified = True
    item = get_object_or_404(Item, id=id)
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
