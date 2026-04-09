from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CustomerViewSet,
    ProductListCreateAPIView,
    ProductDetailAPIView,
    OrderListCreateAPIView,
    OrderDetailAPIView,
    transactions_list_create,
    transactions_detail,
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
    # Products (GenericAPIView)
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    # Orders (GenericAPIView)
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    # Transactions (function-based)
    path('transactions/', transactions_list_create, name='transaction-list-create'),
    path('transactions/<int:pk>/', transactions_detail, name='transaction-detail'),
]
