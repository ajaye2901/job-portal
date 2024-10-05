from django.shortcuts import render
from rest_framework.response import Response
from userapp.permissions import IsCandidateUser
from rest_framework import status
from rest_framework.views import APIView
from .serializers import JobApplicationSerializer
from rest_framework.permissions import AllowAny
from companyapp.models import JobListing
from companyapp.serializers import JobListingSerializers
from django.shortcuts import get_object_or_404
from .models import JobApplication

class JobApplicationView(APIView) :
    permission_classes = [IsCandidateUser]

    def post(self, request) :
        user = request.user
        data = request.data.copy() 
        data['candidate'] = user.id
        serializer = JobApplicationSerializer(data=data)
        if serializer.is_valid() :
            serializer.save(candidate=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AllJobsView(APIView) :
    permission_classes = [IsCandidateUser]

    def get(self, request) :
        jobs = JobListing.objects.filter(is_active = True)
        serializer = JobListingSerializers(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class JobDetailedView(APIView) :
    permission_classes = [IsCandidateUser]

    def get(self, request, job_id):
        job = get_object_or_404(JobListing, id=job_id)
        serializer = JobListingSerializers(job)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AllJobApplicationView(APIView) :
    permission_classes = [IsCandidateUser]

    def get(self, request) :
        user = request.user
        job_applications = JobApplication.objects.filter(candidate=user)
        serializer = JobApplicationSerializer(job_applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class JobApplicationDetailedview(APIView) :
    permission_classes = [IsCandidateUser]

    def get(self, request, application_id) :
        application = get_object_or_404(JobApplication, id=application_id)
        serializer = JobApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class JobApplicationDelete(APIView) :
    permission_classes = [IsCandidateUser]

    def delete(self, request, application_id) :
        application = get_object_or_404(JobApplication, id=application_id)
        application.delete()
        return Response({"message" : "Application deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
