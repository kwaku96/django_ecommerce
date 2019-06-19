from rest_framework.serializers import ModelSerializer
from .models import Item, OrderItem, Order


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'title', 'slug', 'image', 'price',
                  'description', 'discount_price', 'category')


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'item', 'user', 'ordered', 'quantity')


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'ref_code', 'user', 'ordered',
                  'ordered_date', 'start_date', 'items')
