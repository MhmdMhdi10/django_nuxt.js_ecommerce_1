from rest_framework import serializers
from .models import Product
from apps.product.serializers import ProductSerializer


class ProductPhotoSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Product
        fields = ('id', 'product', 'photo',
                  'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted'
                  )
