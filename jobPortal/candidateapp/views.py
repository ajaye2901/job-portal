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
from django.db.models import Q

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
    
class JobApplicationDeleteView(APIView) :
    permission_classes = [IsCandidateUser]

    def delete(self, request, application_id) :
        application = get_object_or_404(JobApplication, id=application_id)
        application.delete()
        return Response({"message" : "Application deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class JobListingFilterView(APIView) :
    permission_classes = [IsCandidateUser]
    def get(self, request):
        queryset = JobListing.objects.all()

        search_query = request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(company__name__icontains=search_query) | 
                Q(location__icontains=search_query)
            )

        salary = request.query_params.get('salary', None)
        if salary:
            queryset = queryset.filter(salary__gte=salary)

        location = request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        serializer = JobListingSerializers(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)