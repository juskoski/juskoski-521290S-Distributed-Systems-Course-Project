from django.contrib import admin
from django.urls import path
from secret_node_app.views import (
    RequestAccessToSecret
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('request-secret/', RequestAccessToSecret, name='request-secret'),
]
