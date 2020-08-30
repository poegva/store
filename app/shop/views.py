import math

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import serializers, viewsets
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.response import Response

from delivery.providers.yandex.plugin import YandexDeliveryPlugin
from payment.utils import get_or_create_payment
from shop.models import Shop, Item, Order, OrderItem


class ItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, item):
        return item.image.url

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'image', 'shop_quantity']


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.order_by('-shop_quantity').all()
    serializer_class = ItemSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']


def validate_enough_items(order_item):
    if order_item['quantity'] > order_item['item'].shop_quantity:
        raise ValidationError('Недостаточно товара')


class OrderItemCreateSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())

    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']
        validators = [validate_enough_items]


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    token = serializers.ReadOnlyField()
    payment = serializers.SerializerMethodField(method_name='get_payment')

    def get_payment(self, order):
        payment, new, reason = get_or_create_payment(order)
        return {
            'token': payment.confirmation_token,
            'cancellation_reason': reason,
            'new': new,
        }

    class Meta:
        model = Order
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'items',
            'address',
            'delivery_type',
            'delivery_extra',
            'token',
            'status',
            'payment',
            'delivery_cost',
            'items_cost',
        ]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        order_serializer = self.get_serializer(data=request.data)
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save(token=get_random_string(length=32), status=Order.WAITING_PAYMENT)

        item_serializer = OrderItemCreateSerializer(data=request.data['items'], many=True)
        item_serializer.is_valid(raise_exception=True)
        order_items = item_serializer.save(order=order)

        order_shops_ids = set()

        for order_item in order_items:
            order_shops_ids.add(order_item.item.shop_id)

            order.items_cost += order_item.quantity * order_item.item.price

            order_item.item.shop_quantity -= order_item.quantity
            order_item.item.save(update_fields=['shop_quantity'])

        if len(order_shops_ids) != 1:
            raise ValidationError('Больше одного магазина в заказе')

        shop = Shop.objects.get(id__in=order_shops_ids)

        optimal_delivery = YandexDeliveryPlugin.get_optimal_option(
            shop, order.delivery_type, order.address, order.items_cost
        )
        order.delivery_cost = math.ceil(optimal_delivery['cost']['deliveryForSender']) if optimal_delivery else 0
        order.shop = shop
        order.save(update_fields=['items_cost', 'delivery_cost', 'shop_id'])

        data = self.get_serializer(order).data

        return Response(data, status=200)

    def retrieve(self, request, pk=None, *args, **kwargs):
        order = get_object_or_404(self.queryset, pk=pk)
        return Response(self.get_serializer(order).data, status=200)
