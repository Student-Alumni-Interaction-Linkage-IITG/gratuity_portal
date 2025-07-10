from django.urls import path
from .views import submit_testimonial, home, professor_list,view_testimonials,thank_you


urlpatterns = [
    path('submit/', submit_testimonial, name='submit_testimonial'),
    path('all/', view_testimonials, name='view_testimonials'),
    path('', home, name='home'),
    path('professors/', professor_list, name='professor_list'),
    path('submit/<int:professor_id>/', submit_testimonial, name='submit_testimonial'),
    path('thank-you/', thank_you, name='thank_you'),

]
