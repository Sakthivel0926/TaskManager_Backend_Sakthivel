from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # REQUIRED
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, default="pending")
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title