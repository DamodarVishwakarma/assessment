from rest_framework import serializers
from django.db import transaction
from .models import Customer, Product, Order, Transaction as Trx


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'amount', 'discount', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        amount = attrs.get('amount', getattr(self.instance, 'amount', 0))
        discount = attrs.get('discount', getattr(self.instance, 'discount', 0))
        if amount is not None and discount is not None and discount > amount:
            raise serializers.ValidationError({'discount': 'Discount cannot exceed amount.'})
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    # Use write-only quantity field for order creation
    quantity = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'product', 'quantity', 'total_amount', 'created_at']
        read_only_fields = ['id', 'total_amount', 'created_at']

    def validate(self, attrs):
        product = attrs.get('product')
        quantity = attrs.get('quantity')
        if product is None or quantity is None:
            return attrs
        if product.quantity < quantity:
            raise serializers.ValidationError({'quantity': 'Insufficient stock for this product.'})
        return attrs

    def create(self, validated_data):
        quantity = validated_data.pop('quantity')
        product = validated_data['product']
        # Compute total_amount = (amount - discount) * quantity
        unit_price = product.amount - product.discount
        total_amount = unit_price * quantity
        with transaction.atomic():
            # Deduct stock
            product.refresh_from_db()
            if product.quantity < quantity:
                raise serializers.ValidationError({'quantity': 'Insufficient stock for this product.'})
            product.quantity -= quantity
            product.save(update_fields=['quantity'])
            order = Order.objects.create(total_amount=total_amount, **validated_data)
        return order


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trx
        fields = ['id', 'order', 'trx_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        order = attrs.get('order')
        if order and hasattr(order, 'transaction'):
            raise serializers.ValidationError({'order': 'This order already has a transaction.'})
        return attrs

