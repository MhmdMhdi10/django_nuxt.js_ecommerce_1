from django.urls import path
from apps.blog.views import (BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView,
                             BlogPostDeleteView, PostReviewListView, PostCommentCreateView, PostCommentUpdateView,
                             PostCommentDeleteView)

app_name = 'product'
urlpatterns = [
    # BLOG
    path('list/', BlogPostListView.as_view()),
    path('detail/<pk>', BlogPostDetailView.as_view()),

    # COMMENT
    path('commnents/list/<post_id>', PostReviewListView.as_view()),
    path('commnents/create/', PostCommentCreateView.as_view()),
    path('commnents/update/<comment_id>', PostCommentUpdateView.as_view()),
    path('commnents/delete/<comment_id>', PostCommentDeleteView.as_view()),

    # ADMIN
    path('create/', BlogPostCreateView.as_view()),
    path('update/<pk>', BlogPostUpdateView.as_view()),
    path('delete/<pk>', BlogPostDeleteView.as_view()),
]
