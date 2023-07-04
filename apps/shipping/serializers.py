from rest_framework import serializers
from .models import Shipping


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ('id', 'city', 'description', 'shipping_method', 'postal_code', 'address', 'shipping_cost',)
