from typing import Any, Dict

from django.shortcuts import redirect

from orders.models import Order


def change_flag(order, attr, msg=None):
    if not msg:
        setattr(order, attr, abs(getattr(order, attr) - 1))
        order.save(update_fields=[attr])
        return redirect('admin_panel:orders')
    setattr(order, attr, True)
    order.save(update_fields=[attr])


def add_count_to_context(context: Dict[str, Any]) -> Dict[str, Any]:
    context.update({
        'count': Order.objects.filter(checked=False).count()
    })
    return context
