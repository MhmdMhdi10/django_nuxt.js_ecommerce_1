import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.user.manager import UserAccountManager

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UserAccount(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    @staticmethod
    def validate_iranian_phone_number(phone_number):
        """
        Validate an Iranian phone number.
        """
        if not re.match(r'^\+98\d{10}$', phone_number):
            raise ValidationError(
                _('Invalid phone number.'),
                params={'phone_number': phone_number},
            )

    username = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(validators=[validate_iranian_phone_number], max_length=13, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def get_phone_number(self):
        return self.phone_number
