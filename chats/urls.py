from django.urls import path
from .views import ListCreateConversation, ListCreateMessage

urlpatterns = [
    path("conversation/", ListCreateConversation.as_view() ),
    path("message/", ListCreateMessage.as_view() )
]