from django.db import models
from professors.models import Professor
from django.contrib.auth.models import User

class Testimonial(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Testimonial by {self.student} for {self.professor}'
