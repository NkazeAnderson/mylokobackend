from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Property, Area, Amenity, Category, Media
from Users.serializers import UserSerializer
from myloko_backend.validators import validateMedia
from chats.models import Conversation
from django.db.models import Q

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
    chatId = serializers.SerializerMethodField()
    class Meta:
        model = Property
        exclude = ("width", "length", "interested_users",  "category")
        include =  [
            "name",
            "category_detail",
            "location",
            "area",
            "street" ,
            "for_sale",
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
        # extra_kwargs = {
        #     "amenities": {"write_only": True},
        #     "location": {"write_only": True},
        # }
    
    def get_interested_users_count(self, obj):
        return obj.interested_users.count()
    
    def get_chatId(self, obj):
        try:
            posted_by = obj.posted_by
            print(posted_by)
            user = self.context.get("request").user
            conversation = Conversation.objects.filter(Q(first_member=posted_by, second_member=user)|Q(first_member=user, second_member=posted_by)).first()
            print(conversation)
            return conversation.id
        except:
            return None
            
    
    def get_video_link(self, obj):
        
        file = Media.objects.filter(property=obj.id, is_video=True).first()
        
        if file:
        
            return "uploads/" + file.file.name #Media.objects.get(property=obj, is_video=True).file
        else:
            return "noimage"
    
    def get_primary_link(self, obj):
       
        file = Media.objects.filter(property=obj.id, is_primary=True).first()
        
        if file:
            return "uploads/" + file.file.name #Media.objects.get(property=obj, is_video=True).file
        else:
            return "noimage"
    
    def get_images_link(self, obj):
        files = Media.objects.filter(property=obj.id, is_video=False)
     
        list = []
        if files:
            
            for file in files.values():
                list.append("uploads/property/" + file.get("file"))
            # print("LIst..............." + file.get("file") )
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
    
class ApartmentRUDSerializer(ApartmentSerializer):
    video =  serializers.FileField(write_only=True, required=False)
    images = serializers.ListField(child=serializers.FileField(max_length=10000, allow_empty_file=False, use_url=False), write_only=True, required=False)
    images_delete = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    primary_image = serializers.FileField(max_length=10000, allow_empty_file=False, use_url=False, write_only=True, required=False)
    new_primary = serializers.IntegerField(required=False, write_only=True)
    primary_deleted = serializers.BooleanField(required=False, write_only=True)
    def get_images_link(self, obj):
        files = Media.objects.filter(property=obj.id, is_primary=False, is_video=False)
        list = []
        if files:
            
            for file in files.values():
                list.append({"url": "/uploads/" + file.get("file"), "id": file.get("id") })
        # print("LIst" + list)
        return list