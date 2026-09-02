from django.db import models


class Professor(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    email_notifications_enabled = models.BooleanField(default=None, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='professors/', blank=True, null=True)
    processed_profile_picture = models.ImageField(upload_to='professors/processed/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
