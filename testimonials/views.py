from django.shortcuts import render, redirect
from .models import Testimonial
from professors.models import Professor
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

# @login_required
# def submit_testimonial(request):
#     if request.method == 'POST':
#         professor_id = request.POST.get('professor')
#         content = request.POST.get('content')
#         professor = Professor.objects.get(id=professor_id)
#         Testimonial.objects.create(professor=professor, student=request.user, content=content)
#         return redirect('/testimonials/submit')
#     professors = Professor.objects.all()
#     return render(request, 'submit_testimonial.html', {'professors': professors})
@login_required
def submit_testimonial(request, professor_id):
    professor = Professor.objects.get(id=professor_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Testimonial.objects.create(
            professor=professor, student=request.user, content=content
        )
        return redirect('thank_you')
    return render(request, 'submit_testimonial.html', {'professor': professor})
def view_testimonials(request):
    testimonials = Testimonial.objects.select_related('professor', 'student').all()
    return render(request, 'testimonials/view_testimonials.html', {'testimonials': testimonials})

def home(request):
    return render(request, 'home.html')
# view prof list 
from professors.models import Professor

@login_required
def professor_list(request):
    professors = Professor.objects.all()
    return render(request, 'professor_list.html', {'professors': professors})
def thank_you(request):
    return render(request, 'thank_you.html')

def logout_view(request):
    logout(request)
    return redirect('home')
