from django.urls import path
from .views import GetUserProfileView, GetUserAddressView, UpdateUserProfileView, CreateAddressView, DeleteAddressView

urlpatterns = [
    path('get/', GetUserProfileView.as_view()),
    path('update/', UpdateUserProfileView.as_view()),
    path('address/get/', GetUserAddressView.as_view()),
    path('address/create/', CreateAddressView.as_view(), name='create-address'),
    path('address/delete/<int:address_id>/', DeleteAddressView.as_view(), name='delete-address'),
]
