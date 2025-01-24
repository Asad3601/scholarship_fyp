# models.py
from django.db import models

class Scholarship(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    due_date = models.CharField(max_length=100)
    link = models.URLField()

    def __str__(self):
        return self.title
