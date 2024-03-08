
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255)
    username=models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    REQUIRED_FIELDS = []

class PeriodDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    symptoms = models.TextField()

    def __str__(self):
        return f"PeriodDetail for {self.user.username} ({self.start_date} to {self.end_date})"

