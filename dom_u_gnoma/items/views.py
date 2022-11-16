from django.shortcuts import get_object_or_404, render

from .models import Item


def catalog(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'items/catalog.html', context)

def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    context = {'item': item}
    return render(request, 'items/item_detail.html', context)
