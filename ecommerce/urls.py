from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.user.urls', namespace="auth")),
    path('categories/', include('apps.category.urls', namespace='category')),
    path('products/', include('apps.product.urls', namespace='product')),
    path('blog/', include('apps.blog.urls', namespace='blog')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('order/', include('apps.order.urls', namespace='order')),
    path('coupon/', include('apps.coupon.urls')),
    path('profile/', include('apps.user_profile.urls')),
    path('wishlist/', include('apps.wishlist.urls')),
    path('review/', include('apps.review.urls')),
    path('shipping/', include('apps.shipping.urls')),
    path('brand/', include('apps.brand.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


