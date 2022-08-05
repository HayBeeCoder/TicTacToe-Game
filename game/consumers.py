import json
from turtle import position
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import channel_layers
from channels.db import database_sync_to_async
from .models import Game, Move

class TicTacToeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_uuid = str(self.scope["url_route"]["kwargs"]["uuid"])
        self.game = await database_sync_to_async(Game.objects.get)(game_uuid = self.game_uuid)
        self.user = self.scope["user"]
        await self.channel_layer.group_add(self.game_uuid, self.channel_name)
        
        await self.accept()


    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        position = text_data["position"]
        move = await database_sync_to_async(self.game.moves.get)(player = self.user)
        await database_sync_to_async(move.positions.append)(position)
        await database_sync_to_async(move.save)()
        print(move)
        is_winner = await database_sync_to_async(self.game.check_winner)()
        if is_winner:
            move = await database_sync_to_async(self.game.moves.get)(player = self.user)
            print(move)
            data = {
                "type":"winner_message",
                "user":str(self.user),
                "position":position
            }
            await self.channel_layer.group_send(self.game_uuid,
                                    data)
        else:
            await database_sync_to_async(self.game.set_current_player)()
        


            

    async def winner_message(self, event):
        await self.send(json.dumps(

            {
                "type":event.get("type"),
                "winner":event.get("user"),
                "position":event.get("position")
            }
        ))

    async def update_board_message(self, event):
        await self.send(json.dumps(
            {
                "player":event.get("player"),
                "position":event.get("position")
            }
        ))



    async def disconnect(self, code):
        return await super().disconnect(code)