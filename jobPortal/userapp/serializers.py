from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Extract the role or default to Candidate if not provided
        role = validated_data.pop('role', User.CANDIDATE)  
        user = User(**validated_data)  # Create a User instance without password hashing
        user.set_password(validated_data['password'])  # Hash the password
        user.role = role  # Set the role
        user.save()  # Save the user to the database
        return user