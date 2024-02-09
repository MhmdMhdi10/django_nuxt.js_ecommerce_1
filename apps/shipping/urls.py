from django.urls import path
from .views import GetShippingView

app_name = 'shipping'
urlpatterns = [
    path('get/', GetShippingView.as_view()),
]
