from django.contrib import admin
from .models import BlogPost, Comment
from apps.core.admin import BaseAdmin  # Import your BaseAdmin class


@admin.register(BlogPost)
class BlogPostAdmin(BaseAdmin):  # Inherit from BaseAdmin
    list_display = ('title', 'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(BaseAdmin):  # Inherit from BaseAdmin
    list_display = ('user', 'post', 'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username', 'post__title')
    raw_id_fields = ('user', 'post', 'reply')
