from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel
from ecommerce.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('rating')
    )
    comment = models.TextField(_('comment'), blank=True, null=True)

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')

    def __str__(self):
        return f'{self.user.username} - {self.rating}'
