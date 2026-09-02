from django.db import models
from professors.models import Professor
from django.contrib.auth.models import User

class Testimonial(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    author_name = models.CharField(max_length=150, default='Anonymous')
    author_designation = models.CharField(max_length=150, blank=True, null=True)
    author_batch = models.CharField(max_length=50, blank=True, null=True)
    author_branch = models.CharField(max_length=100, blank=True, null=True)
    author_email = models.EmailField(max_length=254, blank=True, null=True)
    author_phone = models.CharField(max_length=20, blank=True, null=True)
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f'Testimonial by {self.author_name} for {self.professor}'

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    designation = models.CharField(max_length=150, blank=True, null=True, help_text="e.g., CEO at Google, UG Student")
    batch = models.CharField(max_length=50, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='students/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
