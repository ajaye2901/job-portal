from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import *
from .serializers import CompanySerializers, JobListingSerializers, JobApplicationStatusSerializer
from userapp.permissions import IsEmployerUser
from rest_framework import viewsets     
from candidateapp.models import JobApplication
from candidateapp.serializers import JobApplicationSerializer
from rest_framework.pagination import PageNumberPagination
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

class AllJobApplicationsView(APIView) :
    permission_classes = [IsEmployerUser]

    def get(self, request) :
        user = request.user
        job_applications = JobApplication.objects.filter(job__company__owner=user)

        paginator = PageNumberPagination()
        paginator.page_size = 10

        paginated_application = paginator.paginate_queryset(job_applications, request)
        serializer = JobApplicationSerializer(paginated_application, many=True)
        return paginator.get_paginated_response(serializer.data)

    
class ApplicationStatusChangeView(APIView) :
    permission_classes = [IsEmployerUser]

    def patch(self, request, application_id) :
        application = JobApplication.objects.get(id=application_id)
        serializer = JobApplicationStatusSerializer(application, data=request.data, partial=True)
        if serializer.is_valid() :
            serializer.save()
            return Response({'message' : 'Status Updated'}, status=status.HTTP_200_OK)

