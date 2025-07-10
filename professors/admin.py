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

admin.site.register(Professor)
