from rest_framework import serializers
from .models import Product, ProductDiscount


class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDiscount
        fields = ('id', 'type', 'value')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'photo', 'description',
                  'price', 'count', 'sold', 'created_at')
