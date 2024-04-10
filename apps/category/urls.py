from django.urls import path
from apps.category.views import CategoryListView

app_name = 'category'
urlpatterns = [
    path('list/', CategoryListView.as_view(), name='list'),
]
