from django.db import models


class Professor(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    profile_picture = models.ImageField(upload_to='professors/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
