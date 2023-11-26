from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', "full_name", 'created_at', 'updated_at', 'address', 'zip_code', 'city' ,'state', 'country', 'description']  # Add other fields as needed



