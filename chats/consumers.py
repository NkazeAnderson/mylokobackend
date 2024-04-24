from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class ChatRoomConsumer(AsyncWebsocketConsumer):
        async def connect(self):
                #self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
               
                await self.accept()
                print("Socket Connected")

        async def disconnect(self, close_code):
        # Leave room group
                
                print("Socket Disconnected")
        
        async def receive (self, text_data = None, byte_data = None):
                if (text_data):
                        recievedData = json.loads(text_data)
                        type = recievedData["type"]
                        message = recievedData["message"]
                        data =message["data"]
                        print(data)
                        if type == "join_notifications":
                                room_name = data
                                room_group_name = "notifications_%s" %room_name
                                await self.channel_layer.group_add(room_group_name, self.channel_name)
                                await self.channel_layer.group_send(room_group_name, {'type': "join_notifications", 'message': {'added' : True}})
                        if type == "New_Message":
                                room_name = data
                                room_group_name = "chat_%s" %room_name
                                await self.channel_layer.group_add(room_group_name, self.channel_name)
                                await self.channel_layer.group_send(room_group_name, {'type': "New_Message", 'message': {'chatId' : data}})
                        if type == "Read_Message":
                                print(data)
                                room_name = data["chatId"]
                                room_group_name = "chat_%s" %room_name
                                await self.channel_layer.group_add(room_group_name, self.channel_name)
                                await self.channel_layer.group_send(room_group_name, {'type': "Read_Message", 'message': {'chatId' : data["chatId"], "by": data["by"]}})

        async def join_notifications(self, event):
                await self.send(text_data=json.dumps(event))
        
        async def New_Message(self, event):
                await self.send(text_data=json.dumps(event))
        
        async def Read_Message(self, event):
                await self.send(text_data=json.dumps(event))