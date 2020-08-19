from django.db import models


class Shop(models.Model):
    slug = models.SlugField(verbose_name='Слаг магазина')
    name = models.CharField(max_length=200, verbose_name='Название магазина')

    def __str__(self):
        return self.name


class Item(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')

    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='Стоимость')

    image = models.FileField(upload_to='items', null=True, verbose_name='Изображение')

    def __str__(self):
        return f'{self.name} - {self.shop.name}'


class Order(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя покупателя', blank=True)
    email = models.EmailField(verbose_name='Почта покупателя', blank=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон покупателя', blank=True)

    address = models.JSONField(verbose_name='Адрес покупателя', null=True, blank=True)

    NONE = 'NONE'
    COURIER = 'COURIER'
    POST = 'POST'
    DELIVERY_OPTION_CHOICES = [
        (NONE, 'Не выбрано'),
        (COURIER, 'Курьер'),
        (POST, 'Почта')
    ]
    delivery_option = models.CharField(
        max_length=7, choices=DELIVERY_OPTION_CHOICES, default=NONE, verbose_name='Способ доставки'
    )

    CREATED = 'CREATED'
    WAITING_PAYMENT = 'WAITING_PAYMENT'
    PAYED = 'PAYED'
    STATUS_CHOiCES = [
        (CREATED, 'Создан'),
        (WAITING_PAYMENT, 'Ожидает оплаты'),
        (PAYED, 'Оплачен')
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOiCES, default=CREATED, verbose_name='Статус'
    )

    token = models.CharField(max_length=32, default='NO_TOKEN', verbose_name='Токен доступа к заказу')

    items_cost = models.IntegerField(default=0, verbose_name='Стоимость товаров')
    delivery_cost = models.IntegerField(default=0, verbose_name='Стоимость доставки')

    @property
    def total_cost(self):
        return self.items_cost + self.delivery_cost

    def __str__(self):
        return f'Заказ №{self.pk} ({self.name})'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.item} - {self.quantity} шт. ({self.order})'
