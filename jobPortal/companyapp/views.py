from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import CompanySerializers

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
    permission_classes = [IsAuthenticated]

    def post(self, request) :
        data = request.data.copy()  # Copy request data
        data['owner'] = request.user.id 
        serializer = CompanySerializers(data=data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)