from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from apps.category.models import Category

from django.conf import settings

from apps.core.models import BaseModel

domain = settings.DOMAIN


class Product(BaseModel):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/%Y/%m/')
    description = models.TextField()
    price = models.IntegerField()
    count = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)

    class DiscountType(models.TextChoices):
        PERCENTAGE = 'percentage'
        PRICE = 'price'

    discount_type = models.CharField(
        max_length=10,
        choices=DiscountType.choices,
        default=DiscountType.PERCENTAGE,
        null=True, blank=True
    )
    discount_value = models.IntegerField(null=True, blank=True)

    def get_thumbnail(self):
        if self.photo:
            return domain + self.photo.url

    def __str__(self):
        return self.name


# class ProductDiscount(BaseModel):
#     class Meta:
#         verbose_name = _('Product Discount')
#         verbose_name_plural = _('Product Discounts')
#
#     class DiscountType(models.TextChoices):
#         PERCENTAGE = 'percentage'
#         PRICE = 'price'
#
#     product = models.OneToOneField(Product, on_delete=models.CASCADE)
#     type = models.CharField(
#         max_length=10,
#         choices=DiscountType.choices,
#         default=DiscountType.PERCENTAGE,
#     )
#     value = models.IntegerField()
#
#     def __str__(self):
#         discount = f'{self.value}% off' if self.type == self.DiscountType.PERCENTAGE else (f'${self.value} off '
#                                                                                            f'on {self.product.name}')
#         return f'{discount} _ {self.type} _ {self.product.name}'
#
