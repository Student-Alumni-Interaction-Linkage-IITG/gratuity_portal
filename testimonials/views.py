from django.shortcuts import render, redirect
from .models import Testimonial, StudentProfile
from professors.models import Professor
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Disallow: /profile/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    from professors.models import Professor
    professors = Professor.objects.all()
    base_url = "https://iitg.ac.in/sail/gratitude-portal"
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    xml_lines.append(f'  <url><loc>{base_url}/</loc></url>')
    xml_lines.append(f'  <url><loc>{base_url}/professors/</loc></url>')
    for prof in professors:
        xml_lines.append(f'  <url><loc>{base_url}/submit/{prof.id}/</loc></url>')
    xml_lines.append('</urlset>')
    return HttpResponse("\n".join(xml_lines), content_type="application/xml")


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
def get_or_initialize_student_profile(user):
    profile, created = StudentProfile.objects.get_or_create(user=user)
    changed = False
    
    if not profile.name and (user.get_full_name() or user.username):
        profile.name = user.get_full_name() or user.username
        changed = True
    
    if not profile.email and user.email:
        profile.email = user.email
        changed = True
        
    if changed:
        profile.save()
        
    return profile

import threading
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def send_notification_email_bg(testimonial_id, host_url):
    try:
        # Re-fetch inside thread
        testimonial = Testimonial.objects.get(id=testimonial_id)
        
        # Check preference (must be explicitly True)
        if testimonial.professor.email_notifications_enabled is not True:
            return
            
        # Idempotency check
        if testimonial.email_sent:
            return
            
        student_name = testimonial.author_name or 'A student'
        subject = f'New Testimonial from {student_name}'
        
        message = f"""Dear {testimonial.professor.name},

You have received a new testimonial on the SAIL Gratitude Portal!

From: {student_name}
Department/Batch: {testimonial.author_branch or ''} {testimonial.author_batch or ''}

"{testimonial.content[:150]}{'...' if len(testimonial.content) > 150 else ''}"

Log in to your dashboard to read the full message:
{host_url}/dashboard/

Best regards,
SAIL Team
"""
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [testimonial.professor.email],
            fail_silently=False,
        )
        
        testimonial.email_sent = True
        testimonial.save()
        
    except Exception as e:
        logger.error(f"Failed to send email for testimonial {testimonial_id}: {str(e)}")

def submit_testimonial(request, professor_id=None):
    if not professor_id:
        return redirect('professor_list')
    professor = Professor.objects.get(id=professor_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        author_name = request.POST.get('author_name', '')
        author_designation = request.POST.get('author_designation', '')
        author_batch = request.POST.get('author_batch', '')
        author_branch = request.POST.get('author_branch', '')
        author_email = request.POST.get('author_email', '').strip()
        author_phone = request.POST.get('author_phone', '').strip()
        
        student = None
        if hasattr(request, 'user') and request.user.is_authenticated:
            student = request.user
        
        # Backend validation for required fields
        if not content or not author_name or not author_email or not author_batch:
            context = {'professor': professor, 'error_message': 'Please fill in all required fields, including Batch.', 'default_name': author_name, 'default_email': author_email, 'default_batch': author_batch, 'default_branch': author_branch, 'default_designation': author_designation}
            return render(request, 'submit_testimonial.html', context)
            
        t = Testimonial.objects.create(
            professor=professor,
            student=student,
            content=content,
            author_name=author_name,
            author_designation=author_designation,
            author_batch=author_batch,
            author_branch=author_branch,
            author_email=author_email,
            author_phone=author_phone
        )
        
        # Trigger email in background
        host_url = request.build_absolute_uri('/sail/gratitude_portal')
        thread = threading.Thread(target=send_notification_email_bg, args=(t.id, host_url))
        thread.start()
        
        return redirect('thank_you')
    
    # Pre-fill for authenticated users
    context = {'professor': professor}
    if hasattr(request, 'user') and request.user.is_authenticated:
        profile = get_or_initialize_student_profile(request.user)
        context['default_name'] = profile.name or ''
        context['default_email'] = profile.email or ''
        context['default_designation'] = profile.designation or ''
        context['default_batch'] = profile.batch or ''
        context['default_branch'] = profile.branch or ''
            
    return render(request, 'submit_testimonial.html', context)

def home(request):
    # Auto-redirect professors to their dashboard after login
    if request.user.is_authenticated:
        from professors.models import Professor
        if Professor.objects.filter(email__iexact=request.user.email).exists():
            return redirect('professor_dashboard')
    return render(request, 'home.html')
# view prof list 
from django.db.models import Count
from django.core.paginator import Paginator
import io
import datetime
import re
from django.utils import timezone
from django.http import JsonResponse, FileResponse
from django.contrib import messages

from django.db.models import Q, Value
from django.db.models.functions import Replace

def filter_by_search(queryset, query, *fields):
    """
    Unified fuzzy search utility that strips spaces from both the search query 
    and the database fields to allow flexible matching (e.g., 'ram tej' == 'ramtej').
    """
    if not query:
        return queryset
        
    norm_q = query.replace(' ', '')
    if not norm_q:
        return queryset
        
    annotations = {}
    q_objects = Q()
    
    for field in fields:
        norm_field = f"norm_{field.replace('__', '_')}"
        annotations[norm_field] = Replace(field, Value(' '), Value(''))
        q_objects |= Q(**{f"{norm_field}__icontains": norm_q})
        
    return queryset.annotate(**annotations).filter(q_objects)

def professor_list(request):
    department = request.GET.get('department', '').strip()
    search_query = request.GET.get('q', '').strip()
    
    professors_list = Professor.objects.all()
    if department or search_query:
        if department:
            professors_list = professors_list.filter(department=department)
        if search_query:
            professors_list = filter_by_search(professors_list, search_query, 'name', 'department')
        professors_list = professors_list.order_by('name')
    else:
        # Default landing page: mixture of professors
        professors_list = professors_list.order_by('?')
        
    paginator = Paginator(professors_list, 16) # Show 16 professors per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # All distinct departments for the filter dropdown
    departments = Professor.objects.values_list('department', flat=True).distinct().order_by('department')
    
    return render(request, 'professor_list.html', {
        'page_obj': page_obj,
        'departments': departments,
        'current_department': department,
        'search_query': search_query,
    })

from django.http import JsonResponse
from django.urls import reverse

def professor_search_suggestions(request):
    query = request.GET.get('q', '').strip()
    department = request.GET.get('department', '').strip()
    
    if not query:
        return JsonResponse({'results': []})
        
    qs = Professor.objects.all()
    if department:
        qs = qs.filter(department=department)
        
    qs = filter_by_search(qs, query, 'name', 'department').order_by('name')[:8]
    
    results = []
    for prof in qs:
        image_url = ''
        if prof.profile_picture:
            image_url = prof.profile_picture.url
        elif prof.image_url:
            image_url = prof.image_url
            
        results.append({
            'id': prof.id,
            'name': prof.name,
            'department': prof.department,
            'image_url': image_url,
            'initial': prof.name[0].upper() if prof.name else '?',
            'submit_url': reverse('submit_testimonial', args=[prof.id]),
        })
        
    return JsonResponse({'results': results})
def thank_you(request):
    return render(request, 'thank_you.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def professor_dashboard(request):
    professor = Professor.objects.filter(email__iexact=request.user.email).first()
    if not professor:
        return render(request, 'testimonials/not_a_professor.html')
    
    testimonials_qs = Testimonial.objects.filter(professor=professor).order_by('-submitted_at')
    
    search_query = request.GET.get('q', '').strip()
    testimonials_qs = filter_by_search(testimonials_qs, search_query, 'author_name', 'author_email')
    
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
        'latest_testimonial': latest_testimonial,
        'search_query': search_query,
        'show_notification_popup': professor.email_notifications_enabled is None
    }
    return render(request, 'testimonials/professor_dashboard.html', context)

import json
from django.views.decorators.http import require_POST

@login_required
@require_POST
def update_notification_preference(request):
    try:
        professor = Professor.objects.get(email__iexact=request.user.email)
        data = json.loads(request.body)
        enabled = data.get('enabled')
        if enabled is not None:
            professor.email_notifications_enabled = bool(enabled)
            professor.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    except Professor.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Professor not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

from .forms import StudentProfileForm
from .models import StudentProfile

@login_required
def edit_profile(request):
    profile = get_or_initialize_student_profile(request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('home')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'testimonials/edit_profile.html', {'form': form})

@login_required
def student_dashboard(request):
    profile = get_or_initialize_student_profile(request.user)
    testimonials_list = Testimonial.objects.filter(student=request.user).order_by('-submitted_at')
    
    search_query = request.GET.get('q', '').strip()
    testimonials_list = filter_by_search(testimonials_list, search_query, 'professor__name', 'professor__department')
    
    paginator = Paginator(testimonials_list, 4) # Show 4 per page as in screenshot
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'testimonials/student_dashboard.html', {'profile': profile, 'page_obj': page_obj, 'search_query': search_query})

from django.http import HttpResponseForbidden

@login_required
def delete_testimonial(request, testimonial_id):
    testimonial = Testimonial.objects.get(id=testimonial_id)
    
    is_professor = testimonial.professor.email == request.user.email
    is_student = testimonial.student == request.user
    
    if not (is_professor or is_student):
        return HttpResponseForbidden("You are not allowed to delete this testimonial.")
    
    try:
        testimonial.delete()
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    
    if is_professor:
        return redirect('professor_dashboard')
    else:
        return redirect('student_dashboard')

@login_required
def download_daily_pdf(request):
    professor = Professor.objects.filter(email=request.user.email).first()
    if not professor:
        return JsonResponse({'error': 'Unauthorized access.'}, status=403)
        
    # Get today's bounds in local timezone for the date display
    now = timezone.localtime()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    testimonials = Testimonial.objects.filter(
        professor=professor
    ).order_by('-submitted_at')
    
    if not testimonials.exists():
        return JsonResponse({'error': 'No testimonials received yet.'}, status=400)
        
    context = {
        'professor': professor,
        'testimonials': testimonials,
        'today_date': today_start,
        'total_count': testimonials.count(),
    }
    return render(request, 'testimonials/daily_pdf_print.html', context)

@login_required
def view_student_profile(request, student_id):
    student = User.objects.get(id=student_id)
    profile = StudentProfile.objects.filter(user=student).first()
    return render(request, 'testimonials/student_profile.html', {'student': student, 'profile': profile})

def login_page(request):
    if hasattr(request, 'user') and request.user.is_authenticated:
        return redirect('home')
    
    error_message = None
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')
        
        # Support login with either username or email
        username = username_or_email
        if '@' in username_or_email:
            user_obj = User.objects.filter(email__iexact=username_or_email).first()
            if user_obj:
                username = user_obj.username
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)
            
            next_url = request.GET.get('next') or request.POST.get('next') or 'home'
            return redirect(next_url)
        else:
            error_message = "Invalid email/username or password."
            
    return render(request, 'login.html', {'error_message': error_message})


import json

@login_required
def update_notification_preference(request):
    """API endpoint for professors to update their email notification preference."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    professor = Professor.objects.filter(email=request.user.email).first()
    if not professor:
        return JsonResponse({'error': 'Not a professor account'}, status=403)

    try:
        data = json.loads(request.body)
        enabled = data.get('enabled')
        if not isinstance(enabled, bool):
            return JsonResponse({'error': 'Invalid value for enabled'}, status=400)
        professor.email_notifications_enabled = enabled
        professor.save()
        status_text = 'enabled' if enabled else 'disabled'
        return JsonResponse({'success': True, 'message': f'Email notifications {status_text}.'})
    except (json.JSONDecodeError, Exception) as e:
        return JsonResponse({'error': str(e)}, status=400)
