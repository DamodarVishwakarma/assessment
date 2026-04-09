from rest_framework import viewsets, mixins, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django.db import models

from .models import Customer, Product, Order, Transaction
from .serializers import (
    CustomerSerializer,
    ProductSerializer,
    OrderSerializer,
    TransactionSerializer,
)


class CustomerFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search')

    class Meta:
        model = Customer
        fields = ['search', 'email']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(first_name__icontains=value)
            | models.Q(last_name__icontains=value)
            | models.Q(email__icontains=value)
        )


class ProductFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name='amount', lookup_expr='lte')
    in_stock = filters.BooleanFilter(method='filter_in_stock')

    class Meta:
        model = Product
        fields = ['name', 'min_amount', 'max_amount', 'in_stock']

    def filter_in_stock(self, queryset, name, value):
        if value is True:
            return queryset.filter(quantity__gt=0)
        if value is False:
            return queryset.filter(quantity__lte=0)
        return queryset


class OrderFilter(filters.FilterSet):
    customer = filters.NumberFilter(field_name='customer_id')
    product = filters.NumberFilter(field_name='product_id')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['customer', 'product', 'created_after', 'created_before']


class TransactionFilter(filters.FilterSet):
    trx_id = filters.CharFilter(field_name='trx_id', lookup_expr='icontains')
    order = filters.NumberFilter(field_name='order_id')

    class Meta:
        model = Transaction
        fields = ['trx_id', 'order']


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
    filterset_class = CustomerFilter
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['created_at', 'first_name', 'last_name']


class ProductListCreateAPIView(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               generics.GenericAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filterset_class = ProductFilter
    search_fields = ['name']
    ordering_fields = ['created_at', 'amount', 'quantity']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductDetailAPIView(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filterset_class = ProductFilter
    search_fields = ['name']
    ordering_fields = ['created_at', 'amount', 'quantity']

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class OrderListCreateAPIView(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             generics.GenericAPIView):
    queryset = Order.objects.select_related('customer', 'product').all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    filterset_class = OrderFilter
    ordering_fields = ['created_at', 'total_amount']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OrderDetailAPIView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Order.objects.select_related('customer', 'product').all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    filterset_class = OrderFilter
    ordering_fields = ['created_at', 'total_amount']

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def transactions_list_create(request):
    queryset = Transaction.objects.select_related('order').all()

    # Filtering
    trx_id = request.query_params.get('trx_id')
    if trx_id:
        queryset = queryset.filter(trx_id__icontains=trx_id)
    order_param = request.query_params.get('order')
    if order_param:
        queryset = queryset.filter(order_id=order_param)

    # Ordering (allow only created_at)
    ordering = request.query_params.get('ordering')
    if ordering in ['created_at', '-created_at']:
        queryset = queryset.order_by(ordering)
    else:
        queryset = queryset.order_by('-created_at')

    if request.method == 'GET':
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = TransactionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    if request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def transactions_detail(request, pk):
    try:
        obj = Transaction.objects.select_related('order').get(pk=pk)
    except Transaction.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TransactionSerializer(obj)
    return Response(serializer.data)
