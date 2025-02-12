from channels.generic.websocket import AsyncWebsocketConsumer
import json

class LiveScoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.match_group_name = "live_scores"
        await self.channel_layer.group_add(
            self.match_group_name,
            self.channel_name
        )
        await self.accept()   
             
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.match_group_name,
            self.channel_name
        )
        
    async def send_update(self, event):
        # Receive the data from the view
        message = event['message']
        # print(f"Sending message to WebSocket: {message}")
        await self.send(text_data=json.dumps(message))
        
        # # Debugging: Log the data being sent
        # print(f"Broadcasting message: {message}")
        # print(type(message))

        # Send data to WebSocket clients
        await self.send(text_data=json.dumps({
            'team1': message.get('team1'),
            'team2': message.get('team2'),
            'team1_runs': message.get('team1_runs'),
            'team2_runs': message.get('team2_runs'),
            'team1_wickets': message.get('team1_wickets'),
            'team2_wickets': message.get('team2_wickets'),
            'overs': message.get('overs'),
            'commentary': message.get('commentary'),
        }))