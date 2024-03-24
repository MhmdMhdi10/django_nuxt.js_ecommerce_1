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

    name = models.JSONField(_('name'), default=dict)
    brand = models.JSONField(_('brand'), default=dict)
    description = models.JSONField(_('description'), default=dict)
    counting_unit = models.JSONField(_('counting_unit'), default=dict)

    photo = models.ImageField(upload_to='photos/%Y/%m/')
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

    def get_name(self, language_code):
        return self.name.get(language_code, '')

    def __str__(self):
        # Assuming 'en' as the default language
        return self.get_name('fa')

