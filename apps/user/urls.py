from django.urls import path
from apps.user.views import RegisterUser, RegisterUserVerifyCode

app_name = 'product'
urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('verify/', RegisterUserVerifyCode.as_view()),
]
