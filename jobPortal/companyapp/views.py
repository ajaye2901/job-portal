from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import *
from .serializers import CompanySerializers, JobListingSerializers
from userapp.permissions import IsEmployerUser
from rest_framework import viewsets     

# Create your views here.

"""

Header -> Bearer Token
{
    "name" : "Google",
    "location" : "Banglore",
    "description" : "This is a product based company"
}

"""

class CompanyCreateView(APIView) :
    permission_classes = [IsEmployerUser]

    def post(self, request) :
        data = request.data.copy() 
        data['owner'] = request.user.id 
        serializer = CompanySerializers(data=data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
"""
GET comapny/joblisting/: List all jobs.
POST comapny/joblisting/: Create a new job.
GET comapny/joblisting/{id}/: Retrieve a specific job by ID.
PUT comapny/joblisting/{id}/: Update a specific job by ID.
PATCH comapny/joblisting/{id}/: Partially update a specific job by ID.
DELETE comapny/joblisting/{id}/: Delete a specific job by ID.

"""
 
class JobListingView(viewsets.ModelViewSet) :
    permission_classes = [IsEmployerUser]
    serializer_class = JobListingSerializers
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'Employer':
            return JobListing.objects.filter(company__owner=user)
        return JobListing.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user
        company = Company.objects.filter(owner=user).first()
        serializer.save(company=company)