from rest_framework import serializers
from .models import Conversation, Message
from Users.models import CustomUser
from Users.serializers import UserSerializer
from django.db.models import Q
import json
from rest_framework.response import Response
class ConversationSerializer(serializers.ModelSerializer):
    other_member = serializers.SerializerMethodField()
    unread_messages = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ["id","second_member", "other_member", "unread_messages", "last_message"]
        extra_kwargs = {
            "second_member": {"write_only": True},
        }
    def get_other_member(self, obj):
        try:
            userId = self.context.get("request").user.id
            otherId = obj.first_member.id
            if userId == obj.first_member.id:
                otherId = obj.second_member.id
           
            otherUser = CustomUser.objects.get(pk=otherId)
            return UserSerializer(otherUser).data
            
        except:
            raise serializers.ValidationError(detail="Invalid request", code=400)
    def get_unread_messages(self, obj):
        user = self.context.get("request").user
        return Message.objects.filter(conversation=obj.id, read=False).exclude(sender=user).count()
    
    def get_last_message(self, obj):
        try:
            lastMessage = Message.objects.filter(conversation = obj.id).last()
            print(lastMessage.photo)
            if not lastMessage.photo :
                return {"is_photo": False, "message": lastMessage.message, "date": lastMessage.created_date}
            return {"is_photo": True,  "date": lastMessage.created_date}
        except:
            pass
    
    def validate(self, data):
        data["first_member"] = self.context.get("request").user
        userId = self.context.get("request").user
        try:
            otherMember = CustomUser.objects.get(pk=data["second_member"].id)
            
        except:
           pass 
       
        conversation = Conversation.objects.filter(Q(first_member = userId, second_member = otherMember) | Q(first_member = otherMember, second_member = userId) )
       
        if (conversation.exists()):
            raise serializers.ValidationError(conversation.first().pk, code=200)
        return super().validate(data)
    
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["message", "created_date", "sender", "conversation", "photo", "read"]
        extra_kwargs = {
            "created_date": {"read_only": True},
            "sender": {"read_only": True},
            "photo": {"required": False},
            "message": {"required": False}
        }
    
    def validate(self, attrs):
        try:
            message = attrs["message"]
        except:
            message  = False
        try:
            photo = attrs["photo"]
        except:
            photo = False
        if not message and not photo :
            raise serializers.ValidationError(detail="add a message or photo", code=400)
        attrs["sender"] = self.context.get("request").user
        senderId= self.context.get("request").user.id      
        conversation = attrs["conversation"]
        try:
            first_member = conversation.first_member.pk
            second_member = conversation.second_member.pk
        except:
            raise serializers.ValidationError(detail="Conversation Does not exits", code=404)
        if senderId == first_member or senderId == second_member:
            return super().validate(attrs)  
        else:
            raise serializers.ValidationError(detail="Not a member of this chat", code=400)

            
            
        