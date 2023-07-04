from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.core.admin import BaseAdmin
from .models import Review


@admin.register(Review)
class ReviewAdmin(BaseAdmin):
    list_display = ('id', 'user', 'rating', 'comment',
                    'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    list_filter = ('rating',)
    search_fields = ('user__username', 'comment')
    readonly_fields = ('id',)

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs
