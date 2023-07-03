from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel
from django.conf import settings

User = settings.AUTH_USER_MODEL
domain = settings.DOMAIN


class UserProfile(BaseModel):
    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    image = models.ImageField(upload_to='profiles/%Y/%m/', verbose_name=_('Image'))
    first_name = models.CharField(max_length=255, verbose_name=_('First name'))
    last_name = models.CharField(max_length=255, verbose_name=_('Last name'))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(BaseModel):
    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    body = models.TextField(verbose_name=_('Address'))
    city = models.CharField(
        max_length=255, default='Tehran', verbose_name=_('City'))
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='addresses',
                                     verbose_name=_('User profile'))

    def __str__(self):
        return self.body
