from django.conf import settings
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Cart
from .utils import get_session_cart
from items.models import Item


def add_to_cart(request, id):
    session = request.session
    get_session_cart(session)
    item = Item.objects.get(id=id)
    if request.user.is_authenticated:
        Cart.objects.create(user=request.user, item=item)
    else:
        session[settings.SESSION_CART][str(id)] = 'Добавлен'
        session.modified = True
    return redirect('items:item_detail', id=id)


def delete_from_cart(request, id):
    session = request.session
    get_session_cart(session)
    path = session['path']
    item = Item.objects.get(id=id)
    if request.user.is_authenticated:
        Cart.objects.get(user=request.user, item=item).delete()
    else:
        del session[settings.SESSION_CART][str(id)]
        session.modified = True
    if path == reverse('items:item_detail', kwargs={'id': id}):
        return redirect('items:item_detail', id=id)
    return redirect('cart:items')


def items(request):
    session = request.session
    get_session_cart(session)
    session['path'] = request.path
    session.modified = True
    if request.user.is_authenticated:
        ids = [item['item'] for item in Cart.objects.all().values('item')]
    else:
        ids = session[settings.SESSION_CART].keys()
    items = Item.objects.filter(id__in=ids)
    total_amount = items.aggregate(total=Sum('price'))
    if total_amount['total'] is None:
        total_amount['total'] = 0
    context = {
        'items': items,
        'total_amount': float(total_amount['total'])
    }
    return render(request, 'cart/items.html', context)
