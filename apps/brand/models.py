from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel


class Brand(BaseModel):
    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    name = models.JSONField(_('name'), default={"en": "", "fa": ""})

    description = models.JSONField(_('description'), default={"en": "", "fa": ""})

    country = models.JSONField(_('country'), default={"en": "", "fa": ""})

    picture = models.ImageField(_('picture'), upload_to='brand_photos/%Y/%m/')

    file = models.FileField(_('file'), upload_to='brand_files/%Y/%m/')

    file_2 = models.FileField(_('file_2'), upload_to='brand_files/%Y/%m/', null=True, blank=True)

    def get_name(self, language_code):
        return self.name.get(language_code, '')

    def __str__(self):
        # Assuming 'en' as the default language
        return self.get_name('en')
