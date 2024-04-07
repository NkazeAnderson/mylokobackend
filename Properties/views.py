from rest_framework import generics, authentication, permissions, parsers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Property , Area, Amenity , Category, Media
from .permissions import UpdateAndDestroyPermission
from .serializers import (propertySerializer,
                          LocationSerializer, 
                          CategorySerializer,
                          AmenitySerializer, 
                          ApartmentSerializer,
                          MediaSerializer,
                          ApartmentRUDSerializer
                        )
from os.path import splitext
import json
#from rest_framework import pagination
# Create your views here.

class ListProperty(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = propertySerializer
    authentication_classes= [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
class ListMedia(generics.ListCreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    
class ListCreateApartment(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = ApartmentSerializer
    
    def perform_create(self, serializer):
        images = serializer.validated_data.pop("images")
        video = serializer.validated_data.pop("video")
        primary_image = serializer.validated_data.pop("primary_image")
        category = Category.objects.get(name__iexact = "apartment")
        obj = serializer.save(posted_by = self.request.user, category = category )
        Media.objects.create(property=obj, file=video, is_video=True)
        Media.objects.create(property=obj, file=primary_image, is_primary=True)
        for media in images:
            Media.objects.create(property=obj, file=media)
        
class RetrieveUpdateDestroyApartment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = ApartmentRUDSerializer
    permission_classes =[IsAuthenticated, UpdateAndDestroyPermission]    
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    
    def perform_update(self, serializer):
        
        try:
            images = serializer.validated_data.pop("images")
        except:
            images = False
        try:
            video = serializer.validated_data.pop("video")
        except:
            video = False
        try:
            primary_image = serializer.validated_data.pop("primary_image")
        except:
            primary_image = False
        try:
            images_delete = serializer.validated_data.pop("primary_image")
        except:
            images_delete = False
            
        instance = serializer.save()
        if primary_image:
            try:
                Media.objects.get(property=instance, is_primary=True).delete()
            except:
                Media.objects.create(property=instance, is_primary=True, file=primary_image)
        if video:
            try:
                Media.objects.get(property=instance, is_video=True).delete()
            except:
                Media.objects.create(property=instance, is_video=True, file=video)
        if images:
            for media in images:
                Media.objects.create(property=instance, file=media)
        if images_delete:
            try:
                for target in images_delete:
                    media = Media.objects.get(pk=target)
                    if self.request.user.id == media.property.posted_by.id:
                        media.delete()
                    else:     
                        return Response({"images_delete", "not owner"}, status=status.HTTP_401_UNAUTHORIZED)
                return Response({"action": "deleted medias"}, status=status.HTTP_200_OK)
            except:  
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
class ListLocation(generics.ListAPIView):
    queryset = Area.objects.all()
    serializer_class = LocationSerializer
    pagination_class = None
    
class ListCategory(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

class ListAmenity(generics.ListAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    pagination_class = None

@api_view(["GET"])
def AddInterested(request, **kwargs):
    try:
        property = Property.objects.get(pk=kwargs["pk"])
        is_interested = property.interested_users.filter(id = request.user.id).exists()
        if not is_interested:  
            property.interested_users.add(request.user)
            return Response({"action": "added"}, status=status.HTTP_200_OK)
        property.interested_users.remove(request.user)
        return Response({"action": "removed"}, status=status.HTTP_200_OK)
    except:  
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def RemoveMedia(request, **kwargs):
    print(request.data)
    query = request.data
    print(query["media"])
    try:
        for target in query["media"]:
            medias = Media.objects.get(pk=target)
            if request.user.id == medias.property.posted_by.id:
                medias.delete()
            else:     
                return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"action": "deleted medias"}, status=status.HTTP_200_OK)
    except:  
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    