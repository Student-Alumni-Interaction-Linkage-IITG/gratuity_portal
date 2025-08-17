from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('testimonials.urls')),
    path('admin/', admin.site.urls),
    # path('accounts/', include('social_django.urls', namespace='social')),
]


