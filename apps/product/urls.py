from django.urls import path
from apps.product.views import ListProductsView, ProductDetailView, ListSearchView, ListBySearchView, ListRelatedView

app_name = 'product'
urlpatterns = [
    path('product/<pid>', ProductDetailView.as_view()),
    path('list/', ListProductsView.as_view()),
    path('search', ListSearchView.as_view()),
    path('related/<pid>', ListRelatedView.as_view()),
    path('filter/', ListBySearchView.as_view()),
]
