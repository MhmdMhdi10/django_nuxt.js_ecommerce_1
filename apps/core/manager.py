from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def all_with_deleted(self):
        return super().get_queryset()

    def only_deleted(self):
        return super().get_queryset().filter(is_deleted=True)

    def delete(self):
        return super().update(is_deleted=True, deleted_at=timezone.now())

    def restore(self):
        return super().update(is_deleted=False, deleted_at=None)
