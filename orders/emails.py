from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


def send_order_confirmation_email(order, request=None):
    """
    Send order confirmation email to customer
    """
    # Get the current site domain
    if request:
        site_url = get_current_site(request).domain
    else:
        site_url = 'localhost:8000'  # Default for development

    context = {
        'order': order,
        'site_url': site_url,
    }

    subject = f'Megastation - Confirmación de pedido #{order.id}'
    html_message = render_to_string('orders/email/order_confirmation.html', context)
    plain_message = render_to_string('orders/email/order_confirmation.txt', context)

    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")  # For debugging
        return False


def send_order_status_update_email(order, request=None):
    """
    Send order status update email to customer
    """
    if request:
        site_url = get_current_site(request).domain
    else:
        site_url = 'localhost:8000'

    context = {
        'order': order,
        'site_url': site_url,
    }

    subject = f'Megastation - Actualización de pedido #{order.id}'
    html_message = render_to_string('orders/email/order_status_update.html', context)
    plain_message = render_to_string('orders/email/order_status_update.txt', context)

    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False