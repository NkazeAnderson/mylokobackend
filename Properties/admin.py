from django.contrib import admin
from  .models import Property, Category, Media, Amenity,Division, Area, City, Province, Country

# Register your models here.

admin.site.register(Property)
admin.site.register(Category)
admin.site.register(Media)
admin.site.register(Amenity)
admin.site.register(Area)
admin.site.register(City)
admin.site.register(Province)
admin.site.register(Country)
admin.site.register(Division)