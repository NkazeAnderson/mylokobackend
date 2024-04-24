from rest_framework import generics
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.db.models import Q
from rest_framework import parsers

# Create your views here.

class ListCreateConversation(generics.ListCreateAPIView):
    queryset = Conversation.objects.all().order_by("-id")
    serializer_class = ConversationSerializer
    pagination_class = None
    
    def get_queryset(self):
        userId = self.request.user
        return Conversation.objects.filter(Q(first_member = userId) | Q(second_member = userId) ).order_by("-id")
    
    def perform_create(self, serializer):
        
        userId = self.request.user
        serializer.validated_data["first_member"] = userId
        otherMember = serializer.validated_data["second_member"]
        conversation = Conversation.objects.filter(Q(first_member = userId, second_member = otherMember) | Q(first_member = otherMember, second_member = userId) ).first()
        serializer.save()
        
class UpdateConversation(generics.UpdateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        chatId = kwargs["pk"]
        try:
            conversation = Conversation.objects.get(id = int(chatId))
        except:
            return Response({"Not_ok": "Chat Does Not exits"}, status=400)
        if user == conversation.first_member or user == conversation.second_member:
            conversations = Message.objects.filter(conversation__id= int(chatId)).exclude(sender=user).update(read=True)
            return Response({"Ok": "read"}, status=200)
        else:
            return Response( {"Not_ok": "Not a member of chat"}, status=400)
        
    
    def perform_update(self, serializer):
        user = self.request.user
        chatId = self.kwargs["pk"]
        # print("data")
        print(dir(serializer))
        try:
            conversation = Conversation.objects.get(id = int(chatId))
        except:
            pass
        print( conversation)
        if user == conversation.first_member or user == conversation.second_member:
            conversations = Message.objects.filter(conversation__id= int(chatId)).exclude(sender=user).update(read=True)
        

class ListCreateMessage(generics.ListCreateAPIView):
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    serializer_class = MessageSerializer
    pagination_class = None
    
    def get_queryset(self, ):
        try:
            
            conversationId = self.request.query_params["conversationId"]
            range = self.request.query_params["range"]
            if range == "all":
                return Message.objects.filter(conversation__id = conversationId).order_by("id")
            else:
                return Message.objects.filter(conversation__id = conversationId , read=False).order_by("id")
        except:
            pass
        
        try:
            conversationId = self.request.query_params["conversationId"]
            return Message.objects.filter(conversation__id = conversationId).order_by("id")
        except:
            pass
        
        try:
            user = self.request.user
            range = self.request.query_params["range"]
            conversations = Message.objects.filter(Q(conversation__first_member = user) | Q(conversation__second_member = user)).order_by("id")
            return conversations.filter(read=False)
        except:
            return Message.objects.none()