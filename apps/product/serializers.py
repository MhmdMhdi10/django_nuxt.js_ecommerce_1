from rest_framework import serializers
from .models import Product
from apps.category.serializers import CategorySerializer
from apps.brand.serializers import BrandSerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'brand', 'slug', 'photo', 'description',
                  'counting_unit', 'counting_unit_2', 'counting_unit_3',
                  'price', 'count', 'sold', 'created_at', 'discount_type',
                  'discount_value', 'get_thumbnail')
