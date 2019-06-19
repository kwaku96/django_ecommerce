from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from core.models import Order, OrderItem, Item
from core.serializers import (
    OrderItemSerializer,
    ItemSerializer,
    OrderSerializer
)


class ItemList(ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetail(RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
