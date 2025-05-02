from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import CustomRegistrationSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CustomRegistrationSerializer, UserProfileSerializer

User = get_user_model()

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomRegistrationSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']  # Only allow POST requests (registration)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Create user
            return Response(
                {
                    "message": "User registered successfully",
                    "user": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Retrieve the authenticated user

    def list(self, request, *args, **kwargs):
        """ Restrict listing, return only the current user's profile. """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)