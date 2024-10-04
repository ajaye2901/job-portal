from django.db import models
from companyapp.models import *
from userapp.models import User
# Create your models here.

class JobApplication(models.Model) :
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected")
    ]
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Candidate'})
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self) :
        return f"{self.job.title} - {self.candidate.username}"


