# from django.contrib import admin

# # Register your models here.
# from .models import Testimonial

# @admin.register(Testimonial)
# class TestimonialAdmin(admin.ModelAdmin):
#     list_display = ('professor', 'student', 'submitted_at')
#     list_filter = ('professor', 'submitted_at')
#     search_fields = ('content',)
from django.contrib import admin
from .models import Professor
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Professor

@admin.register(Professor)
class ProfessorAdmin(ImportExportModelAdmin):
    pass

# admin.site.register(Professor)
