from django.urls import path
from .views import ListCreateConversation, ListCreateMessage, UpdateConversation

urlpatterns = [
    path("conversation/", ListCreateConversation.as_view() ),
    path("message/", ListCreateMessage.as_view() ),
    path("conversation/<int:pk>/", UpdateConversation.as_view() )
]