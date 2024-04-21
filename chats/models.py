from django.db import models
from Users.models import CustomUser
# Create your models here.
class Conversation (models.Model):
    first_member = models.ForeignKey(CustomUser, related_name="chat_first_member", on_delete=models.DO_NOTHING)
    second_member = models.ForeignKey(CustomUser, related_name="chat_second_member", on_delete=models.DO_NOTHING)
    def __str__(self):
        return f"{self.first_member.first_name} with {self.second_member.first_name}"

    class Meta:
        unique_together = ("first_member", "second_member")
class Message (models.Model):
    conversation = models.ForeignKey(Conversation, related_name="chat_first_member", on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=250)
    photo = models.FileField(upload_to="chats")
    sender = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    read = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.conversation.pk} - {self.created_date.day}/{self.created_date.month}/{self.created_date.year} - {self.created_date.hour}:{self.created_date.minute}"
    
