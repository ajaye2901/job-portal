from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny

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
