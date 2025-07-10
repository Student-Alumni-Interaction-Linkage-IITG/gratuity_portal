# from django.contrib import admin

# # Register your models here.
# import csv
# from django.http import HttpResponse

# @admin.action(description='Export Testimonials as CSV')
# def export_testimonials(modeladmin, request, queryset):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="testimonials.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['Professor', 'Student', 'Content', 'Date'])
#     for t in queryset:
#         writer.writerow([t.professor.name, t.student.username, t.content, t.submitted_at])
#     return response
from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('professor', 'student', 'submitted_at')
    list_filter = ('professor', 'submitted_at')
    search_fields = ('content',)
