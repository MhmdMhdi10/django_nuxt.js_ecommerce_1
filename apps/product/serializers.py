from rest_framework import serializers
from .models import Product
from apps.category.serializers import CategorySerializer
from apps.brand.serializers import BrandSerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'brand', 'slug', 'photo', 'description', 'garantee', "popularity",
                  'counting_unit', 'price', 'count', 'sold', 'created_at', 'discount_type', 'updated_at',
                  'discount_value', 'get_thumbnail')
