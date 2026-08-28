from django.urls import path
from .views import (
    submit_testimonial, home, professor_list, professor_search_suggestions, 
    thank_you, logout_view, professor_dashboard, edit_profile, 
    delete_testimonial, view_student_profile, student_dashboard, login_page,
    download_daily_pdf
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_page, name='login_page'),
    path('submit/', submit_testimonial, name='submit_testimonial'),
    path('professors/', professor_list, name='professor_list'),
    path('professors/suggestions/', professor_search_suggestions, name='professor_search_suggestions'),
    path('submit/<int:professor_id>/', submit_testimonial, name='submit_testimonial'),
    path('thank-you/', thank_you, name='thank_you'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', professor_dashboard, name='professor_dashboard'),
    path('profile/', student_dashboard, name='student_dashboard'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('testimonial/delete/<int:testimonial_id>/', delete_testimonial, name='delete_testimonial'),
    path('student/<int:student_id>/', view_student_profile, name='view_student_profile'),
    path('dashboard/download-daily-pdf/', download_daily_pdf, name='download_daily_pdf'),
]
