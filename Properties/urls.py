from django.urls import path
from .views import (ListProperty,
                    ListLocation, 
                    ListCategory,
                    ListAmenity, 
                    ListCreateApartment, 
                    RetrieveUpdateDestroyApartment, AddInterested,ListMedia)


urlpatterns = [
    path('property/', ListProperty.as_view(),  name='property_list'),
    path('property/apartment/', ListCreateApartment.as_view()),
    path('property/apartment/<int:pk>/', RetrieveUpdateDestroyApartment.as_view(), name='apartment_detail'),
    path('property/apartment/<int:pk>/interested', AddInterested),
    path('location/', ListLocation.as_view()),
    path('category/', ListCategory.as_view()),
    path('amenity/', ListAmenity.as_view()),
    path('media/', ListMedia.as_view()),
]