from django.contrib import admin
from django.urls import path
from login_node_app.views import (
    GetUserDetails, CreateUser, LoginUser, GetActiveSessions
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', GetUserDetails, name='user-list'),
    path('register/', CreateUser, name='user-register'),
    path('login/', LoginUser, name='user-login'),
    path('active-sessions/', GetActiveSessions, name='active-sessions')
]
