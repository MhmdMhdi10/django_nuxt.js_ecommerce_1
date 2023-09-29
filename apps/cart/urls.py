from django.urls import path

from apps.cart.views import (GetItemsView, AddItemView, UpdateItemView, GetTotalView, GetTotalCount,
                             RemoveItemView, EmptyCartView, SynchCartView)


app_name = 'product'
urlpatterns = [


    # ADMIN
    path('view/', GetItemsView.as_view()),
    path('add/', AddItemView.as_view()),
    path('update/', UpdateItemView.as_view()),
    path('total/', GetTotalView.as_view()),
    path('count/', GetTotalCount.as_view()),
    path('remove/', RemoveItemView.as_view()),
    path('empty/', EmptyCartView.as_view()),
    path('sync/', SynchCartView.as_view()),
]
