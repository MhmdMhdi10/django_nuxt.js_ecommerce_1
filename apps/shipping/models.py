from django.db import models
from apps.core.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Shipping(BaseModel):
    SHIPPING_METHODS = (
        ('Post', _('Post')),
        ('SnapBike', _('Snap Bike')),
        ('CargoTransport', _('cargo transport')),
        ('PrivateShipping', _('private')),
    )

    city = models.CharField(max_length=255)
    description = models.TextField()
    shipping_method = models.CharField(max_length=20, choices=SHIPPING_METHODS)

    postal_code = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    shipping_cost = models.IntegerField()

    def __str__(self):
        return f'{self.city} ({self.shipping_method}) \n ({self.description})'
