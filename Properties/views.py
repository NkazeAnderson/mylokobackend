from rest_framework import generics, authentication, permissions, parsers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Property , Area, Amenity , Category, Media
from .permissions import UpdateAndDestroyPermission
from django.db.models import Q
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
from rest_framework.filters import OrderingFilter
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
    queryset = Property.objects.all().order_by("-id")
    serializer_class = ApartmentSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    
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
            
    def post(self, request, *args, **kwargs):
        print(request.data)
        print(".............")
        print(self.request.content_type)
        return super().post(request,  *args, **kwargs)
    
    def get_queryset(self):
        print("")
        q = Property.objects.all().order_by("-id")
        try:
         queryPrice =  int(self.request.query_params["price"]) 
         q = q.filter(price__lte = queryPrice)
        except:
            pass
        
        try:
         queryBed =  int(self.request.query_params["bed"]) 
         q = q.filter(bed_rooms__lte = queryBed)
        except:
            pass
        
        try:
         queryKitchen =  int(self.request.query_params["kitchen"]) 
         q = q.filter(internal_kitchens__lte = queryKitchen)
        except:
            pass
        
        try:
         queryToilet =  int(self.request.query_params["toilet"]) 
         q = q.filter(internal_toilets__lte = queryToilet)
        except:
            pass
        
        
        try:
         queryLocation =  self.request.query_params["location"]
         q = q.filter(Q(location__name__icontains = queryLocation) | Q(location__city__name__icontains = queryLocation)| Q(street__icontains = queryLocation))
        except:
            print("err location")
            pass
        
        
        
        return q
    
    
class RetrieveUpdateDestroyApartment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = ApartmentRUDSerializer
    permission_classes =[IsAuthenticated, UpdateAndDestroyPermission]    
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def perform_update(self, serializer):
        print(serializer.validated_data)
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
            images_delete = serializer.validated_data.pop("images_delete")
        except:
            images_delete = False
        try:
            new_primary = serializer.validated_data.pop("new_primary")
        except:
            new_primary = False
        try:
            primary_deleted = serializer.validated_data.pop("primary_deleted")
        except:
            primary_deleted = False
            
        instance = serializer.save()
        print("images.........." , images)
        
        if primary_image and new_primary:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        if primary_image:
            try:
                if primary_deleted:
                    Media.objects.filter(property=instance, is_primary=True).first().delete()
                else:
                    media = Media.objects.get(property=instance, is_primary=True)
                    media.is_primary=False
                    media.save()
                    
                Media.objects.create(property=instance, is_primary=True, file=primary_image)
            except:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
                
        if video:
            try:
                Media.objects.filter(property=instance, is_video=True).first().delete()
                Media.objects.create(property=instance, is_video=True, file=video)
            except:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
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
            except:  
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_primary:
            try:
                print("New Primary")
                media = Media.objects.get(pk=new_primary)
                print("New media...", media)
                print()
                print(primary_deleted)
                if primary_deleted:
                    print("Deleting")
                    Media.objects.filter(property=instance, is_primary=True).first().delete()
                    print("Deleted")
                else:
                    oldPrimary = Media.objects.get(property=instance, is_primary=True)
                    print(oldPrimary, media )
                    oldPrimary.is_primary=False
                    oldPrimary.save()
                if self.request.user.id == media.property.posted_by.id:
                    print("True......... req eql id")
                    media.is_primary = True
                    media.save()
                else:     
                    return Response({"images_delete", "not owner"}, status=status.HTTP_401_UNAUTHORIZED)
            except:  
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        allMedia = Media.objects.filter(property=instance)
        for val in allMedia:
            print("Isprimary", val.is_primary)
            #print("Isprimary", val.is_primary)
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
    