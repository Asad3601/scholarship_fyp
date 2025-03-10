from django.db import models

class UserModel(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords securely in real apps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
    
class SavedSchaolarship(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # Adjust User model as needed
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    due_date = models.CharField(max_length=100)
    link = models.URLField()
    degrees = models.CharField(max_length=255, default='Masters,Bachelors')

    def __str__(self):
        return self.title
