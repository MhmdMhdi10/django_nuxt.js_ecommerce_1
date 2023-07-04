from django.db import models
from apps.core.models import BaseModel
from apps.product.models import Product
from ecommerce import settings

User = settings.AUTH_USER_MODEL


class Wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    products = models.ManyToManyField(Product, related_name='wishlists')

    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return f'{self.user.username}\'s wishlist'
