from channels.generic.websocket import AsyncWebsocketConsumer

class ChatRoomConsumer(AsyncWebsocketConsumer):
        async def connect(self):
                self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
                
                self.room_group_name = "chat_%s" % self.room_name
                print(self.scope)
                # Join room group
                #await self.channel_layer.group_add(self.room_group_name, self.channel_name)

                await self.accept()

        async def disconnect(self, close_code):
        # Leave room group
                await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
                