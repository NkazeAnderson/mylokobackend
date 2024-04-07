from django.urls import path
from .views import CreateUser , RetrieveFull, RetrieveUpdateDestroy, ListProperties
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('user/<int:id>/properties/', ListProperties.as_view()),
    path('user/<int:pk>/', RetrieveUpdateDestroy.as_view()),
    path('user/myinfo/', RetrieveFull.as_view()),
    path('user/signup/', CreateUser.as_view()),
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]