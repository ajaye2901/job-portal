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