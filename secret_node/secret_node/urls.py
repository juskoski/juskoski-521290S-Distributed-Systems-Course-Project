from django.contrib import admin
from django.urls import path
from secret_node_app.views import (
    RequestAccessToSecret,
    CreateSecret,
    GetSecretNames,
    StartVote,
    GetVotes,
    GiveVote
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('request-secret/', RequestAccessToSecret, name='request-secret'),
    path('create-secret/', CreateSecret, name='create-secret'),
    path('get-secret-names/', GetSecretNames, name='get-secret-names'),
    path('start-vote/', StartVote, name='start-vote'),
    path('get-votes/', GetVotes, name='get-votes'),
    path('give-vote/', GiveVote, name='give-vote'),
]
