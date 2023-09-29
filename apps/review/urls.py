from django.urls import path
from .views import (GetProductReviewsView, GetProductReviewView, CreateProductReviewView, UpdateProductReviewView,
                    DeleteProductReviewView, FilterProductReviewsView)

urlpatterns = [
    path('list/<productId>', GetProductReviewsView.as_view()),
    path('user/reviews/<productId>', GetProductReviewView.as_view()),
    path('create/<productId>', CreateProductReviewView.as_view()),
    path('update/<productId>', UpdateProductReviewView.as_view()),
    path('delete/<productId>', DeleteProductReviewView.as_view()),
    path('filter/<productId>', FilterProductReviewsView.as_view()),
]
