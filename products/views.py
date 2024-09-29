from rest_framework import viewsets, permissions
from django.core.cache import cache
from django.db.models import Q
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination



class ProductPagination(PageNumberPagination):
    page_size = 10


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allows read access to non-admins

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = cache.get('product_list')
        if queryset is None:
            # queryset = Product.objects.select_related('category').all()
            queryset = Product.objects.select_related('category').order_by('id')  # Order products by id
            cache.set('product_list', queryset, timeout=3600)  # Cache for 1 hour

        category = self.request.query_params.get('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        in_stock = self.request.query_params.get('in_stock')

        if category:
            queryset = queryset.filter(category__name=category)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if in_stock:
            queryset = queryset.filter(stock__gt=0)

        return queryset

    def perform_update(self, serializer):
        instance = serializer.save()
        cache.delete('product_list')  # Invalidate cache on update

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete('product_list')  # Invalidate cache on delete