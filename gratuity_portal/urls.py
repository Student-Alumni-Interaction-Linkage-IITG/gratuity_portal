from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('testimonials.urls')),
    path('admin/', admin.site.urls),
]
# /auth/login/google-oauth2/

# /auth/login/azuread-oauth2/

# /auth/logout/

