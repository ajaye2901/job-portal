from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser) :
    CANDIDATE = 'Candidate'
    EMPLOYER = 'Employer'
    ADMIN = 'Admin'

    ROLE_CHOICES = [
        (CANDIDATE, 'Candidate'),
        (EMPLOYER, 'Employer'),
        (ADMIN, 'Admin')
    ]
    role = models.CharField(max_length=20, default='Candidate')

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.ADMIN
        super(User, self).save(*args, **kwargs)