from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.user.urls', namespace="auth")),

    path('docs/', schema_view),
]
