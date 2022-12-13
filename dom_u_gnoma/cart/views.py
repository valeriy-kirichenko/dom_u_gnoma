from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse

from .utils import add_delete_from_cart, get_cart_items, get_session_cart


def add_to_cart(request, id):
    add_delete_from_cart(request, id)
    return redirect('items:item_detail', id=id)


def delete_from_cart(request, id):
    add_delete_from_cart(request, id, add=False)
    if request.session['path'] == reverse(
        'items:item_detail', kwargs={'id': id}
    ):
        return redirect('items:item_detail', id=id)
    return redirect('cart:items')


def items(request):
    session = request.session
    get_session_cart(session)
    session['path'] = request.path
    session.modified = True
    user = request.user
    items = get_cart_items(user, session)
    total_amount = items.aggregate(total=Sum('price'))
    if total_amount['total'] is None:
        total_amount['total'] = 0
    context = {
        'items': items,
        'total_amount': "{:.2f}".format(total_amount['total'])
    }
    return render(request, 'cart/items.html', context)
