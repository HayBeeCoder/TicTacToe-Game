import json
from typing import Tuple
from channels.generic.websocket import WebsocketConsumer
from channels.layers import channel_layers
from channels.db import database_sync_to_async
from .models import Game, Move
from asgiref.sync import sync_to_async ,async_to_sync

class TicTacToeConsumer(WebsocketConsumer):
    def connect(self):
        self.game_uuid = str(self.scope["url_route"]["kwargs"]["uuid"])
        self.game = Game.objects.get(game_uuid = self.game_uuid)
        self.user = self.scope["user"]
        async_to_sync(self.channel_layer.group_add)(self.game_uuid, self.channel_name)
        self.players =  self.game.players.all()
        self.accept()
        if self.user not in self.players:
            self.game.add_new_player(self.user)
            self.game.set_current_player()

            async_to_sync(self.channel_layer.group_send)(self.game_uuid, {
                   "type":"initialize_current_player",
                   "current_player":str(self.game.current_player),
                   "other_player":str(self.game.player_2)                   }
            )
        



    def receive(self, text_data=None, bytes_data=None):
        if self.game.status == "finished":
            return
        text_data = json.loads(text_data)
        position = text_data["position"]
        print(text_data)
        move = self.game.moves.get(player = self.user)
        move.positions.append(position)
        
        move.save()
        player_mark = move.player_mark
        if self.game.current_player.username != text_data["player"]:
            return

        async_to_sync(self.channel_layer.group_send)(self.game_uuid, {
            "type":"update_board",
            "position":position,
            "current_player":text_data["player"],
            "player_mark":player_mark
            
        })

        is_winner = self.game.check_winner()
        if isinstance(is_winner, Tuple):
            move = self.game.moves.get(player = self.user)
            data = {
                "type":"winner_message",
                "user":str(self.user),
                "position":position,
                "winning_moves":list(is_winner[1])
            }
            async_to_sync(self.channel_layer.group_send)(self.game_uuid,
                                    data)
        

    def winner_message(self, event):
        self.send(json.dumps(

            {
                "type":event.get("type"),
                "winner":event.get("user"),
                "position":event.get("position"),
                "winning_moves":event.get("winning_moves")
            }
        ))

    def update_board(self, event):
        self.game.set_current_player()
        next_player =self.game.current_player
        print( {"current_player":event.get("current_player"),
                "next_player":str(next_player),})
        self.send(json.dumps(
            {
                "type":"update_board_message",
                "current_player":event.get("current_player"),
                "position":event.get("position"),
                "next_player":str(next_player),
                "player_mark":event.get("player_mark")
            }
        ))

    def initialize_current_player(self, event):
        self.send(
            json.dumps(event)
        )



    def disconnect(self, code):
        return super().disconnect(code)