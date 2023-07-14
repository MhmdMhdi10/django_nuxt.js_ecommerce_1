from django.urls import path
from apps.user.views import RegisterUser

app_name = 'product'
urlpatterns = [
    path('register/', RegisterUser.as_view()),
]
