from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_order_message(message):
    context = {
        'id': message.order.id,
        'first_name': message.order.first_name,
        'text': message.text
    }
    subject = render_to_string('email/order_message_subject.txt', context)
    body_text = render_to_string('email/order_message_body.txt', context)
    send_mail(
        subject,
        body_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[message.order.email]
    )


def order_checked_dispatcher(sender, **kwargs):
    send_order_message(kwargs['instance'])
