from rest_framework import serializers
from .models import Company, JobListing
from candidateapp.models import JobApplication

class CompanySerializers(serializers.ModelSerializer) :
    class Meta :
        model = Company
        fields = "__all__"

class JobListingSerializers(serializers.ModelSerializer) :
    class Meta :
        model = JobListing
        fields = "__all__"
        read_only_fields = ['company']

class JobApplicationStatusSerializer(serializers.ModelSerializer) :
    class Meta:
        model = JobApplication
        fields = ['status']