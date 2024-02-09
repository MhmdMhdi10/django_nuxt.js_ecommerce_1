from django.db import models
from apps.core.models import BaseModel
from apps.product.models import Product

from django.conf import settings

User = settings.AUTH_USER_MODEL


class Cart(BaseModel):

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product, through='CartItem')

    def add_product(self, product, count=1):
        cart_product, created = CartItem.objects.get_or_create(cart=self, product=product)
        if not created:
            cart_product.count += count
            cart_product.save()
        else:
            cart_product.count = count
            cart_product.save()
        self.update_total_price()

    def remove_product(self, product):
        cart_product = CartItem.objects.get(cart=self, product=product)
        cart_product.delete()
        self.update_total_price()

    def update_total_price(self):
        cart_products = CartItem.objects.filter(cart=self)
        total_price = sum([cart_product.product.price * cart_product.count for cart_product in cart_products])
        self.total_price = total_price
        self.save()


class CartItem(BaseModel):

    class Meta:
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):

        self.price = self.product.price * self.count
        super(CartItem, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.count} x {self.product.name} in cart'
