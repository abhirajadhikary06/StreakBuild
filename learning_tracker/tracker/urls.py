from django.urls import path
from . import views

urlpatterns = [
    # Landing Page (Default Route)
    path('', views.landing_page, name='landing_page'),  # Root URL points to landing page

    # Authentication URLs
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    # Profile and Field of Interest URLs
    path('field-of-interest/', views.field_of_interest, name='field_of_interest'),
    path('profile/', views.profile, name='profile'),

    # Dashboard and File URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload-file/', views.upload_file, name='upload_file'),
    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),

    # Notification URLs
    path('mark-notifications-as-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
]