from django.urls import path
from apps.brand.views import BrandListView ,BrandDetailView

app_name = 'brand'
urlpatterns = [
    path('list/', BrandListView.as_view(), name='list'),
    path('get/<pid>', BrandDetailView.as_view(), name='detail'),
]
