import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.user.manager import UserAccountManager

from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class UserAccount(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    username = models.CharField(max_length=255, unique=True)

    phone_regex = RegexValidator(regex=r'^(\+989|09)\d{9}$',
                                 message=_(
                                     "Phone number must be entered in the format: '+989xxxxxxxxx' or '09xxxxxxxxx'."))
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def get_phone_number(self):
        return self.phone_number


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'
