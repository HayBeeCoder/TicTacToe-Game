import json
from typing import Tuple
from channels.generic.websocket import WebsocketConsumer
from channels.layers import channel_layers
from channels.db import database_sync_to_async

from game.bot import BotPlay
from .models import Game, Move, User
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
                   "other_player":str(self.game.player_2)}
            )
        



    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)

        if self.game.status == "Finished":
            return
        

        if str(self.game.current_player) != text_data["player"]:
            print(self.game.current_player , text_data["player"])
            return
        position = text_data["position"]
        print(text_data)
        move = self.game.moves.get(player = self.user)
        move.positions.append(position)
        
        move.save()
        player_mark = move.player_mark
        

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


class TicTacToeBOTConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope["user"]
        self.game_uuid = str(self.scope["url_route"]["kwargs"]["uuid"])
        self.game = Game.objects.get(game_uuid = self.game_uuid)
        self.game.set_current_player()
        self.bot_player = User.objects.get(username="BOT")
    
        self.accept()


    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        if self.game.status == "Finished":
            return

        
        player_position = text_data["position"]
        player_move = self.game.moves.get(player = self.user)
        player_move.positions.append(player_position)
            
        player_move.save()
        player_mark = player_move.player_mark

        is_winner = self.game.check_winner()
        if isinstance(is_winner, Tuple):
            self.send(json.dumps(

                {
                "player_position":player_position,
                "type":"winner_message",
                "winning_moves":list(is_winner[1])
            }
            ))
            return
          
        self.game.set_current_player()


        bot_player_move = self.game.moves.get(player = self.bot_player)
        bot_player_positions = list(bot_player_move.positions)

        botPlayer = BotPlay(
            bot_moves= list(bot_player_positions)[:],
            player_moves= list(player_move.positions)[:]
            )
        bot_move =botPlayer.check_player_win_move(botPlayer.bot_moves,
                                                  botPlayer.player_moves  )
        if isinstance(bot_move, str):
            print("We are here")
            bot_player_move.positions.append(bot_move)
            bot_player_move.save()


        else:
            bot_move =botPlayer.check_player_win_move(botPlayer.player_moves,
                                                      botPlayer.bot_moves)
            if isinstance(bot_move, str):
                bot_player_move.positions.append(bot_move)
                bot_player_move.save()
                
            else:
                bot_move = botPlayer.play_in_the_middle_or_elsewhere()
                bot_player_move.positions.append(bot_move)
                bot_player_move.save()


        bot_mark = bot_player_move.player_mark
          

        self.send(json.dumps(
            {
                "type":"bot_update_board_message",
                "player_position":player_position,
                "bot_position":bot_move,
                "player_mark":player_mark,
                "bot_mark":bot_mark
             }
            ))
        


        is_winner = self.game.check_winner()
        if isinstance(is_winner, Tuple):
            self.send(json.dumps(

                {
                "bot_position":bot_move,
                "type":"winner_message",
                "winning_moves":list(is_winner[1])
            }
            ))
            return
        self.game.set_current_player()
        
        
    
    def disconnect(self, code):
        return super().disconnect(code)