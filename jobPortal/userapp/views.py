from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer
from .permissions import IsAdminUser
from companyapp.models import JobListing
from companyapp.serializers import JobListingSerializers
from django.shortcuts import get_object_or_404
from candidateapp.models import JobApplication
from candidateapp.serializers import JobApplicationSerializer

User = get_user_model()

# Create your views here.

class AdminLoginView(APIView) :
    permission_classes = [AllowAny]

    def post(self, request) :
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)

        if user is not None :
            if user.role ==  "Admin" :
                access_token = AccessToken.for_user(user)
                return Response({
                    'access' : str(access_token),
                    'message' : 'Admin logged in'
                })
            else :
                return Response({'error' : 'You are not autherized'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'error' : 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    

"""

{
"username" : "ajay",
"email" : "ajaye@gmail.com",
"password" : "ajaye@123",
"role" : "Employer"
}

{
"username" : "Messi",
"email" : "Messi@gmail.com",
"password" : "messi@123",
"role" : "Candidate"
}   

"""
    
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.role in ["Employer", "Candidate", "Admin"]:
                access_token = AccessToken.for_user(user)
                return Response({
                    'access': str(access_token),
                    'message': f'{user.role} logged in successfully'
                })
            else:
                return Response({'error': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    

"""
Admin Functionalities

"""

class AdminAllJobsView(APIView) :
    permission_classes = [IsAdminUser]

    def get(self, request) :
        jobs = JobListing.objects.all()
        serializer = JobListingSerializers(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, job_id) :
        job = get_object_or_404(JobListing, id=job_id)
        job.delete()
        return Response({"message" : "Job deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class AdminJobApplicationsView(APIView) :
    permission_classes = [IsAdminUser]

    def get(self, request) :
        applications = JobApplication.objects.all()
        serializer = JobApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, application_id) :
        application = get_object_or_404(JobApplication, id=application_id)
        application.delete()
        return Response({"message" : "job Application Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class AllUsersView(APIView) :
    permission_classes = [IsAdminUser]

    def get(self, request) :
        users = User.objects.exclude(role='Admin')
        serializer = UserRegistrationSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, user_id) :
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response({'message' : 'User deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)

