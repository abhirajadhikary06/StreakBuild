from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/')),  # Redirect root URL to login page
    path('', include('tracker.urls')),  # Include app-specific URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)