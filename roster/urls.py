from django.urls import path
# from .views import (image_upload, mark_attendance, roster_create_view,
#                     roster_delete_view, roster_list_view, roster_update_view,user_register)
from .views import register,roster_create_view

urlpatterns = [
    path('register/',register,name="register"),
    # path('roster/', roster_list_view, name='roster_list_url'),
    path('roster/add/', roster_create_view, name='roster_create_url'),
    # path('roster/<int:id>/edit/', roster_update_view, name='roster_update_url'),
    # path('roster/<int:id>/delete/', roster_delete_view, name='roster_delete_url'),
    # path('roaster/mark_attendance/', mark_attendance, name='mark_attendance'),
    # path('image_capture/', image_upload, name='image_upload'),
]


