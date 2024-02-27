
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    # Your other urls
]
