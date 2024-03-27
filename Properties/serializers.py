from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Property, Area, Amenity, Category, Media
from Users.serializers import UserSerializer
from myloko_backend.validators import validateMedia

class propertySerializer (serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    url_link = serializers.HyperlinkedIdentityField(view_name="apartment_detail")
    poster = serializers.CharField(source="posted_by.first_name", read_only=True)
    class Meta:
        model = Property
        fields = "__all__"
    def get_url(self, obj):
        return reverse("apartment_detail", kwargs={"id": obj.id})

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "id"]

class MediaSerializer (serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"

class AmenitySerializer (serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["name", "id"]

class LocationSerializer (serializers.ModelSerializer):
    city_name = serializers.CharField(read_only=True, source="city")
    class Meta:
        model = Area
        exclude = ["city"]
   
class ApartmentSerializer (serializers.ModelSerializer):
    posted_by = UserSerializer(read_only=True)
    is_interested = serializers.SerializerMethodField()
    amenities_details = serializers.SerializerMethodField()
    category_detail = serializers.CharField(read_only=True, source="category")
    interested_users_count = serializers.SerializerMethodField()
    area = serializers.CharField(read_only=True, source="location")
    video =  serializers.FileField(write_only=True)
    video_link = serializers.SerializerMethodField()
    images = serializers.ListField(child=serializers.FileField(max_length=10000, allow_empty_file=False, use_url=False), write_only=True)
    primary_image = serializers.FileField(max_length=10000, allow_empty_file=False, use_url=False, write_only=True)
    primary_link = serializers.SerializerMethodField()
    images_link = serializers.SerializerMethodField()
    class Meta:
        model = Property
        exclude = ("width", "length", "interested_users",  "category")
        include =  [
            "name",
            "category_detail",
            "location",
            "area",
            "street" ,
            "posted_by", 
            "is_interested,"
            "amenities" ,
            "amenities_details",
            "bed_rooms",
            "sitting_rooms",
            "internal_toilets",
            "internal_kitchens",
            "price" ,
            "caution",
            "created_date"]
        read_only_fields = ["posted_by"]
        extra_kwargs = {
            "amenities": {"write_only": True},
            "location": {"write_only": True},
        }
    
    def get_interested_users_count(self, obj):
        return obj.interested_users.count()
    
    def get_video_link(self, obj):
        
        file = Media.objects.filter(property=obj.id, is_video=True).first()
        
        if file:
            return "/uploads/" + file.file.name #Media.objects.get(property=obj, is_video=True).file
        else:
            return "/noimage"
    
    def get_primary_link(self, obj):
       
        file = Media.objects.filter(property=obj.id, is_primary=True).first()
        
        if file:
            return "/uploads/" + file.file.name #Media.objects.get(property=obj, is_video=True).file
        else:
            return "/noimage"
    
    def get_images_link(self, obj):
        files = Media.objects.filter(property=obj.id, is_primary=False, is_video=False)
        list = []
        if files:
            
            for file in files.values():
                list.append("/uploads/" + file.get("file"))
        # print("LIst" + list)
        return list
    
    def get_is_interested(self, obj):
        return obj.interested_users.filter(id = self.context.get("request").user.id ).exists()
        
    def get_amenities_details(self, obj):
        return [i.name for i in obj.amenities.all()]
    
    def validate_video(self, value):
        validateMedia(media=value , type="video")
        return value
        
    def validate_primary_image(self, value):
        validateMedia(media=value , type="image")
        return value
    
    
    def validate_images(self, value):
        for image in value:
            validateMedia(media=image , type="image")
        return value
    
    
      

