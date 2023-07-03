from rest_framework import serializers
from .models import Product, ProductDiscount


class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDiscount
        fields = ('id', 'type', 'value')


class ProductSerializer(serializers.ModelSerializer):
    discount = ProductDiscountSerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'photo', 'description', 'price', 'discount', 'count', 'sold')

    def create(self, validated_data):
        discount_data = validated_data.pop('discount', None)
        product = Product.objects.create(**validated_data)
        if discount_data:
            ProductDiscount.objects.create(product=product, **discount_data)
        return product

    def update(self, instance, validated_data):
        discount_data = validated_data.pop('discount', None)
        discount = instance.discount

        instance.category = validated_data.get('category', instance.category)
        instance.name = validated_data.get('name', instance.name)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.count = validated_data.get('count', instance.count)
        instance.sold = validated_data.get('sold', instance.sold)

        instance.save()

        if discount_data:
            if discount:
                discount.type = discount_data.get('type', discount.type)
                discount.value = discount_data.get('value', discount.value)
                discount.save()
            else:
                ProductDiscount.objects.create(product=instance, **discount_data)
        elif discount:
            discount.delete()

        return instance
