from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet,OrderDetailView


router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),  # This will include the routes for the ViewSet
    # You can add other paths if needed
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),  # Detail view for a specific order

]