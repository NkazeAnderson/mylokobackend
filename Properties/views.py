from rest_framework import generics, authentication, permissions, parsers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Property , Area, Amenity , Category, Media
from .permissions import UpdateAndDestroyPermission
from .serializers import propertySerializer,LocationSerializer, CategorySerializer, AmenitySerializer, ApartmentSerializer,MediaSerializer
from os.path import splitext
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
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    
    def perform_create(self, serializer):
        images = serializer.validated_data.pop("images")
        video = serializer.validated_data.pop("video")
        primary_image = serializer.validated_data.pop("primary_image")
        category = Category.objects.get(name = "apartment")
        obj = serializer.save(posted_by = self.request.user, category = category.id )
        Media.objects.create(property=obj, file=video, is_video=True)
        Media.objects.create(property=obj, file=primary_image, is_primary=True)
        for media in images:
            Media.objects.create(property=obj, file=media)
            
class RetrieveUpdateDestroyApartment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes =[IsAuthenticated, UpdateAndDestroyPermission]
    
class ListLocation(generics.ListAPIView):
    queryset = Area.objects.all()
    serializer_class = LocationSerializer
    
class ListCategory(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ListAmenity(generics.ListAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

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