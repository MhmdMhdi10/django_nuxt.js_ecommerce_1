from rest_framework import serializers
from .models import Wishlist
from apps.product.serializers import ProductSerializer
from apps.product.models import Product


class WishlistSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'user', 'products', 'created_at', 'updated_at',)
        read_only_fields = ('id', 'created_at', 'updated_at',)

    def create(self, validated_data):
        products_data = validated_data.pop('products', [])
        wishlist = Wishlist.objects.create(**validated_data)
        for product_data in products_data:
            product = Product.objects.get(id=product_data['id'])
            wishlist.products.add(product)
        return wishlist

    def update(self, instance, validated_data):
        products_data = validated_data.pop('products', [])
        instance = super().update(instance, validated_data)
        instance.products.clear()
        for product_data in products_data:
            product = Product.objects.get(id=product_data['id'])
            instance.products.add(product)
        return instance
