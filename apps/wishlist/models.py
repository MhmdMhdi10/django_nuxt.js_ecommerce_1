from django.db import models
from apps.core.models import BaseModel
from apps.product.models import Product  # Import the Product model
from ecommerce import settings

User = settings.AUTH_USER_MODEL


class Wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, related_name='wishlist', through="WishlistItem")

    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return f'{self.user.username}\'s wishlist'


class WishlistItem(BaseModel):
    class Meta:
        verbose_name = 'WishlistItem'
        verbose_name_plural = 'WishlistItems'

    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
