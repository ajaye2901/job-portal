from django.db import models
from userapp.models import User

# Create your models here.

class Company(models .Model) :
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"role": "Employer"}, related_name='Company_owner')
    name = models.CharField(max_length=100) 
    location = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class JobListing(models.Model) :
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.IntegerField()
    location = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.title