from rest_framework import serializers
from .models import *

class JobApplicationSerializer(serializers.ModelSerializer) :
    class Meta:
        model = JobApplication
        fields = "__all__"
        read_only_fields = ['candidate']