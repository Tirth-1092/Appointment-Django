from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model 
# from .models import User

User = get_user_model()   # retrieves the project's active User model

class CustomRegistrationSerializer(UserCreateSerializer):
    confirm_password = serializers.CharField(write_only=True,style={'input_type': 'password'}  # 👈 This makes it a password field
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}}  # 👈 Mask password too

    def validate(self, data):
        if data['password'] != data.pop('confirm_password', None): # Remove confirm_password before saving
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)     
    

class UserProfileSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ['id', 'username',  'first_name', 'last_name', 'email', 'phone_number']
        read_only_fields = ['id']  # Users cannot modify these fields       