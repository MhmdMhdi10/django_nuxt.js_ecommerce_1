from django.urls import path
from .views import CheckCouponView

urlpatterns = [
    path('check/', CheckCouponView.as_view()),
]
