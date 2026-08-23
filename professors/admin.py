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
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if 'profile_picture' in form.changed_data and obj.profile_picture:
            from .utils import process_teacher_photo
            process_teacher_photo(obj)

# admin.site.register(Professor)
