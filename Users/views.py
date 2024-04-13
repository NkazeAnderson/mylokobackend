from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import UserSerializer, UserFullSerializer
from .models import CustomUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .permissions import UpdateAndDestroyPermission
from Properties.models import Property
from Properties.serializers import ApartmentSerializer
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

    

class RetrieveFull (generics.ListAPIView):
    serializer_class = UserFullSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        print("self.request..............")
        print(self.request)
        return CustomUser.objects.filter(id= self.request.user.id)
    
    
class ListProperties (generics.ListAPIView):
    serializer_class = ApartmentSerializer
    queryset = Property.objects.filter(posted_by__pk = 9)

    def get_queryset(self):
        print(self.kwargs)
        return Property.objects.filter(posted_by__pk = self.kwargs["id"])
    

# def ListProperties(request, *args, **kwargs):
    
#     properties =  Property.objects.filter(posted_by__pk = user_id)
#     print(properties)
#     props = ApartmentSerializer(instance=properties[0],)
#     print(props.data)
#     return Response({"pkkk": "kakskaks"}) 
    
