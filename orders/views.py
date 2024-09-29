from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        for item in order.orderitem_set.all():
            product = item.product
            product.stock -= item.quantity
            product.save()

    def perform_update(self, serializer):
        order = serializer.save()
        if 'status' in serializer.validated_data:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{order.user.id}",
                {
                    'type': 'order_status_update',
                    'message': f'Your order #{order.id} status has been updated to {order.status}'
                }
            )


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)