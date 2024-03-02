from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import register,register_success_view,homepage,custom_login,custom_logout,create_roster,roster_list,roster_delete_view,roster_update_view,mark_attendance,no_access,roster_attendance_display

urlpatterns = [
    path('register/',register,name="register"),
    path('roster_list/', roster_list, name='roster_list_url'),
    path('register/success/', register_success_view, name='register_success'),
    path('',homepage,name="homepage"),
    path('login/',custom_login,name='custom_login'),
    path('logout/',custom_logout,name='custom_logout'),
    path('create_roster/',create_roster,name='create_roster'),
    path('roster/<int:id>/edit/', roster_update_view, name='roster_update_url'),
    path('roster/<int:id>/delete/', roster_delete_view, name='roster_delete_url'),
    path('roster/<int:id>/<str:working_days>/<str:shift>/attendance/', roster_attendance_display, name='roster_attendance_url'),
    path('mark_attendance/',mark_attendance,name="mark_attendance"),
    path('no_access/',no_access,name='no_access'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

