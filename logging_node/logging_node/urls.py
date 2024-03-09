from django.contrib import admin
from django.urls import path
from logging_node_app.views import PostLog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logging/', PostLog, name='post-log'),
]
