from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class BaseModelManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def active(self):
        return super().get_queryset().filter(is_deleted=False)

    def deleted(self):
        return super().get_queryset().filter(is_deleted=True)

    def delete(self):
        return super().update(is_deleted=True, deleted_at=timezone.now())

    def restore(self):
        return super().update(is_deleted=False, deleted_at=None)

    def hard_delete(self):
        super().delete()
