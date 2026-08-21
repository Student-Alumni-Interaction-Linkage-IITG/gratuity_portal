from django.urls import path
from .views import manage_professors

urlpatterns = [
    path('manage/', manage_professors, name='manage_professors'),
]
