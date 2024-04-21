from django.db import models
from Users.models import CustomUser

class Category (models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.name}"

class Country (models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.name}"

class Province (models.Model):
    name = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}, {self.country}"

class Division (models.Model):
    name = models.CharField(max_length=20)
    province= models.ForeignKey(Province, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}, {self.province}"

class City (models.Model):
    name = models.CharField(max_length=20)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}, {self.division}"

class Area (models.Model):
    name = models.CharField(max_length=20)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}, {self.city}"



class Amenity (models.Model):
    name = models.CharField(max_length=15)
    def __str__(self):
        return f"{self.name}"



class Property(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    location= models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    street = models.CharField(max_length=40) 
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    interested_users = models.ManyToManyField(CustomUser, related_name="interestedUsers", blank=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    bed_rooms = models.PositiveSmallIntegerField(blank=True, null=True)
    sitting_rooms = models.PositiveSmallIntegerField(blank=True, null=True)
    internal_toilets = models.PositiveSmallIntegerField(blank=True, null=True)
    internal_kitchens = models.PositiveSmallIntegerField(blank=True, null=True)
    width = models.PositiveSmallIntegerField(blank=True, null=True)
    length = models.PositiveSmallIntegerField(blank=True, null=True)
    price = models.IntegerField()
    for_sale = models.BooleanField(default=False)
    caution = models.IntegerField(default=0, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.street} {self.location}"
    

class Media (models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    file = models.FileField(upload_to= "property")
    is_primary = models.BooleanField(default=False)
    is_video = models.BooleanField(default=False)

