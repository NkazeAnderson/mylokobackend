from django.urls import path
from .views import (ListProperty,
                    ListLocation, 
                    ListCategory,
                    ListAmenity, 
                    ListCreateApartment, 
                    RetrieveUpdateDestroyApartment, 
                    AddInterested,
                    ListMedia,
                    RemoveMedia,
                    GetInterested
                    )


urlpatterns = [
    path('property/', ListProperty.as_view(),  name='property_list'),
    path('property/apartment/', ListCreateApartment.as_view()),
    path('property/apartment/<int:pk>/', RetrieveUpdateDestroyApartment.as_view(), name='apartment_detail'),
    path('property/apartment/<int:pk>/interested/', AddInterested),
    path('property/interested/', GetInterested.as_view()),
    path('locations/', ListLocation.as_view()),
    path('categories/', ListCategory.as_view()),
    path('amenities/', ListAmenity.as_view()),
    path('media/',RemoveMedia),
]