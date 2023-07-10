from rest_framework import serializers
from .models import Cart, CartItem
from apps.product.serializers import ProductSerializer
from apps.product.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'price')


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'total_price', 'cart_items')

    def create(self, validated_data):
        cart_items_data = validated_data.pop('cart_items')
        cart = Cart.objects.create(**validated_data)
        for cart_item_data in cart_items_data:
            product_data = cart_item_data.pop('product')
            product = Product.objects.get(pk=product_data.get('id'))
            cart_item = CartItem.objects.create(cart=cart, product=product, **cart_item_data)
        return cart

    def update(self, instance, validated_data):
        cart_items_data = validated_data.pop('cart_items')
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        existing_cart_items = CartItem.objects.filter(cart=instance)
        existing_cart_items_ids = [item.id for item in existing_cart_items]
        for cart_item_data in cart_items_data:
            if 'id' in cart_item_data:
                # Update existing cart item
                if cart_item_data['id'] in existing_cart_items_ids:
                    cart_item = existing_cart_items.get(id=cart_item_data['id'])
                    cart_item.product = Product.objects.get(pk=cart_item_data['product']['id'])
                    cart_item.quantity = cart_item_data.get('quantity', cart_item.quantity)
                    cart_item.save()
            else:
                # Create new cart item
                product_data = cart_item_data.pop('product')
                product = Product.objects.get(pk=product_data.get('id'))
                CartItem.objects.create(cart=instance, product=product, **cart_item_data)
        # Delete any cart items that were not updated or created in the request
        existing_cart_items.exclude(id__in=[item_data.get('id', -1) for item_data in cart_items_data]).delete()
        return instance
