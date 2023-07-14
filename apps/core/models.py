from django.db import models
from django.utils.translation import gettext_lazy as _
from ecommerce.settings import AUTH_USER_MODEL
from django.utils import timezone
from apps.core.manager import BaseModelManager


User = AUTH_USER_MODEL


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('is deleted'))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('deleted at'))
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='%(class)s_created_by', verbose_name=_('created by'),
                                   null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='%(class)s_updated_by', verbose_name=_('updated by'),
                                   null=True, blank=True)

    objects = BaseModelManager()

    class Meta:
        abstract = True
        verbose_name = _('Base Model')
        verbose_name_plural = _('Base Models')

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        super().delete()
