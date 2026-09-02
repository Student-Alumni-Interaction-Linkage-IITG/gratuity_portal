from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.urls import re_path
from django.views.static import serve
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('testimonials.urls')),
    path('professors_admin/', include('professors.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('social_django.urls', namespace='social')),
    
    # Serve media files directly (needed for production without Nginx)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    
    # SEO
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
