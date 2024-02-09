from django.urls import path
from .views import GetWishlistItemsView, AddItemToWishlistView, GetTotalItemsInWishlistView, RemoveItemFromWishlistView

urlpatterns = [
    path('list/', GetWishlistItemsView.as_view()),
    path('add/', AddItemToWishlistView.as_view()),
    path('total/', GetTotalItemsInWishlistView.as_view()),
    path('remove/', RemoveItemFromWishlistView.as_view()),
]
