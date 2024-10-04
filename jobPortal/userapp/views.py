from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer

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