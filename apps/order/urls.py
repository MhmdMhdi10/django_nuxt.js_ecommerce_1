from django.urls import path
from .views import ListOrdersView, ListOrderDetailView

app_name = "order"

urlpatterns = [
    path('list/', ListOrdersView.as_view()),
    path('detail/<transactionId>', ListOrderDetailView.as_view()),
]
