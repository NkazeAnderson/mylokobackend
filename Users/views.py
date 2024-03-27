from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import UserSerializer
from .models import CustomUser
from .permissions import UpdateAndDestroyPermission
# Create your views here.

class CreateUser (generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    def perform_create(self, serializer):
        password = serializer.validated_data.get("password")
        phone = serializer.validated_data.get("phone")
        first_name = serializer.validated_data.get("first_name")
        last_name = serializer.validated_data.get("last_name")
        user = CustomUser.objects.create(phone= phone, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return 

class RetrieveUpdateDestroy (generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes =[permissions.IsAuthenticated, UpdateAndDestroyPermission]