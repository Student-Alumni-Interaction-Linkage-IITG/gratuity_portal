from django.urls import path
from .views import submit_testimonial, home, professor_list, thank_you, logout_view, professor_dashboard, edit_profile, delete_testimonial, view_student_profile, student_dashboard

urlpatterns = [
    path('submit/', submit_testimonial, name='submit_testimonial'),
    path('', home, name='home'),
    path('professors/', professor_list, name='professor_list'),
    path('submit/<int:professor_id>/', submit_testimonial, name='submit_testimonial'),
    path('thank-you/', thank_you, name='thank_you'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', professor_dashboard, name='professor_dashboard'),
    path('profile/', student_dashboard, name='student_dashboard'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('testimonial/delete/<int:testimonial_id>/', delete_testimonial, name='delete_testimonial'),
    path('student/<int:student_id>/', view_student_profile, name='view_student_profile'),
]
