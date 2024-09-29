import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.channel_layer.group

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(f"user_{self.user.id}", self.channel_name)

    async def receive_order_status(self, event):
        await self.send(text_data=json.dumps({
            'status': event['status']
        }))