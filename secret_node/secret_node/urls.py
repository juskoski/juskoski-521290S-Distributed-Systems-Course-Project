from django.contrib import admin
from django.urls import path
from secret_node_app.views import (
    RequestAccessToSecret,
    CreateSecret,
    GetSecretNames,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('request-secret/', RequestAccessToSecret, name='request-secret'),
    path('create-secret/', CreateSecret, name='create-secret'),
    path('get-secret-names/', GetSecretNames, name='get-secret-names'),
]
