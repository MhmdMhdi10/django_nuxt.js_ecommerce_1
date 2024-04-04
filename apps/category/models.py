from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel


class Category(BaseModel):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)
    name = models.JSONField(_('name'), default={"en": "", "fa": ""})

    def get_name(self, language_code):
        return self.name.get(language_code, '')

    def __str__(self):
        # Assuming 'en' as the default language
        return self.get_name('en')
