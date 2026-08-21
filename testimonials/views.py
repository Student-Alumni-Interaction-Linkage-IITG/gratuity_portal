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
def submit_testimonial(request, professor_id):
    professor = Professor.objects.get(id=professor_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        author_name = request.POST.get('author_name', '')
        author_designation = request.POST.get('author_designation', '')
        author_batch = request.POST.get('author_batch', '')
        author_branch = request.POST.get('author_branch', '')
        
        student = None
        if request.user.is_authenticated:
            student = request.user
            if not author_name:
                author_name = request.user.get_full_name() or request.user.username
            try:
                profile = request.user.student_profile
                if not author_designation: author_designation = profile.designation
                if not author_batch: author_batch = profile.batch
                if not author_branch: author_branch = profile.branch
            except Exception:
                pass
                
        Testimonial.objects.create(
            professor=professor,
            student=student,
            content=content,
            author_name=author_name,
            author_designation=author_designation,
            author_batch=author_batch,
            author_branch=author_branch
        )
        return redirect('thank_you')
    
    # Pre-fill for authenticated users
    context = {'professor': professor}
    if request.user.is_authenticated:
        context['default_name'] = request.user.get_full_name() or request.user.username
        try:
            profile = request.user.student_profile
            context['default_designation'] = profile.designation
            context['default_batch'] = profile.batch
            context['default_branch'] = profile.branch
        except Exception:
            pass
            
    return render(request, 'submit_testimonial.html', context)

def home(request):
    return render(request, 'home.html')
# view prof list 
from professors.models import Professor

from django.core.paginator import Paginator

def professor_list(request):
    department = request.GET.get('department')
    if department:
        professors_list = Professor.objects.filter(department=department).order_by('name')
    else:
        professors_list = Professor.objects.all().order_by('name')
        
    paginator = Paginator(professors_list, 12) # Show 12 professors per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # We still need all departments for the filter pills
    all_professors = Professor.objects.all()
    
    return render(request, 'professor_list.html', {'page_obj': page_obj, 'professors': all_professors, 'current_department': department})
def thank_you(request):
    return render(request, 'thank_you.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def professor_dashboard(request):
    professor = Professor.objects.filter(email=request.user.email).first()
    if not professor:
        return render(request, 'testimonials/not_a_professor.html')
    
    testimonials_qs = Testimonial.objects.filter(professor=professor).order_by('-submitted_at')
    
    # Calculate stats
    total_testimonials = testimonials_qs.count()
    unique_students = testimonials_qs.values('student').distinct().count()
    latest_testimonial = testimonials_qs.first()
    
    paginator = Paginator(testimonials_qs, 5) # Show 5 per page as in screenshot
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'professor': professor,
        'page_obj': page_obj,
        'total_testimonials': total_testimonials,
        'unique_students': unique_students,
        'latest_testimonial': latest_testimonial
    }
    return render(request, 'testimonials/professor_dashboard.html', context)

from .forms import StudentProfileForm
from .models import StudentProfile

@login_required
def edit_profile(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'testimonials/edit_profile.html', {'form': form})

@login_required
def student_dashboard(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    testimonials_list = Testimonial.objects.filter(student=request.user).order_by('-submitted_at')
    
    paginator = Paginator(testimonials_list, 4) # Show 4 per page as in screenshot
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'testimonials/student_dashboard.html', {'profile': profile, 'page_obj': page_obj})

from django.http import HttpResponseForbidden

@login_required
def delete_testimonial(request, testimonial_id):
    testimonial = Testimonial.objects.get(id=testimonial_id)
    
    is_professor = testimonial.professor.email == request.user.email
    is_student = testimonial.student == request.user
    
    if not (is_professor or is_student):
        return HttpResponseForbidden("You are not allowed to delete this testimonial.")
    
    testimonial.delete()
    
    if is_professor:
        return redirect('professor_dashboard')
    else:
        return redirect('student_dashboard')

@login_required
def view_student_profile(request, student_id):
    student = User.objects.get(id=student_id)
    profile = StudentProfile.objects.filter(user=student).first()
    return render(request, 'testimonials/student_profile.html', {'student': student, 'profile': profile})
