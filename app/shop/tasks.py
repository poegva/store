
from celery.task import task
from django.core.mail import send_mail
from django.db.models import F
from django.utils import timezone

from shop.models import Order, OrderNotification
from shop.utils import send_template_mail


@task()
def cancel_unpayed_orders():
    orders_to_cancel = Order.objects.filter(
        status=Order.WAITING_PAYMENT,
        shop__isnull=False,
        shop__payment_max_time__isnull=False,
        created__lt=timezone.now() - timezone.timedelta(minutes=1) * F('shop__payment_max_time')
    )
    for order in orders_to_cancel:
        order.cancel()


@task()
def send_order_mails():
    notifications = (
        OrderNotification.objects
        .filter(status=OrderNotification.REQUESTED)
        .select_related('order', 'order__shop')
    )
    for notification in notifications:
        order = notification.order

        send_template_mail(
            order.email,
            f'Заказ {notification.order.id} оформлен',
            'order_mail',
            {'order': order, 'first_name': order.name.split()[0], 'items': order.items.all()},
            order.shop.noreply_email_address,
            order.shop.noreply_email_password
        )

        notification.status = OrderNotification.SENT
        notification.save(update_fields=['status'])

