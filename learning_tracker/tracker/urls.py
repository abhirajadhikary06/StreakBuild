from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('profile/', views.profile, name='profile'),
    path('delete-image/<int:image_id>/', views.delete_image, name='delete_image'),  # Add this line
    path('mark-notifications-as-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
]