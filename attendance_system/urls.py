
from django.contrib import admin
from django.urls import include, path

from .views import (roster_create_view, roster_delete_view, roster_list_view,
                    roster_update_view)

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('roster/', roster_list_view, name='roster_list_url'),
    path('roster/add/', roster_create_view, name='roster_create_url'),
    path('roster/<int:id>/edit/', roster_update_view, name='roster_update_url'),
    path('roster/<int:id>/delete/', roster_delete_view, name='roster_delete_url'),
    # Your other urls
]
