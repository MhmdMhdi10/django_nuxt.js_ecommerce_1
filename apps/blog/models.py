from django.db import models
from apps.core.models import BaseModel
from django.conf import settings

User = settings.AUTH_USER_MODEL


class BlogPost(BaseModel):
    title = models.CharField(max_length=200, verbose_name='Title')
    content = models.TextField(verbose_name='Content')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'


class Comment(BaseModel):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, verbose_name='Post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    text = models.TextField(verbose_name='Text')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Reply')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
