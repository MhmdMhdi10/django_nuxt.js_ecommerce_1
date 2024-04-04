from rest_framework import serializers
from .models import Product
from apps.category.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'slug', 'photo', 'description',
                  'price', 'count', 'sold', 'created_at', 'discount_type',
                  'discount_value', 'get_thumbnail')
