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
