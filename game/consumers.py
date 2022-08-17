import json
from typing import Tuple
from channels.generic.websocket import WebsocketConsumer
from channels.layers import channel_layers
from channels.db import database_sync_to_async
from django.contrib.sessions.models import Session
from django.conf import settings
from game.bot import BotPlay
from .models import Game, Move, User
from asgiref.sync import sync_to_async ,async_to_sync

class TicTacToeConsumer(WebsocketConsumer):
    def connect(self):
        self.user = Session.objects.get(session_key = self.scope["session"].session_key)

        self.game_uuid = str(self.scope["url_route"]["kwargs"]["uuid"])
        self.game = Game.objects.get(game_uuid = self.game_uuid)
        #self.user = self.scope["user"]
        async_to_sync(self.channel_layer.group_add)(self.game_uuid, self.channel_name)
        self.players =  self.game.players.all()
        self.accept()
        
        if self.user not in self.players:
            self.game.add_new_player(self.user)
            self.game.set_current_player()

            async_to_sync(self.channel_layer.group_send)(self.game_uuid, {
                   "type":"initialize_current_player",
                   "current_player":str(self.game.current_player.get_decoded()["user"]),
                   "other_player":str(self.game.player_2.get_decoded()["user"])}
            )
        



    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        if text_data["type"] == "play_again":
            self.game.clear_game_data()

            async_to_sync(self.channel_layer.group_send)(self.game_uuid, 
                {
                    "type":"reload_page"
                }
            )
          
            return
        print(self.scope["session"]["user"])
        if self.game.status == "Finished":
            return
        
        current_player = str(self.game.current_player.get_decoded()["user"])

        if current_player != text_data["player"]:
            print(current_player,text_data["player"])
            return
        position = text_data["position"]
        move = self.game.moves.get(player = self.user)
        move.positions.append(position)
        
        move.save()
        player_mark = move.player_mark

        self.game.check_draw()
        async_to_sync(self.channel_layer.group_send)(self.game_uuid, {
            "type":"update_board",
            "position":position,
            "current_player":current_player,#text_data["player"],
            "player_mark":player_mark
            
            
        })

        is_winner = self.game.check_winner()
        print(self.game.move_count)

        if isinstance(is_winner, Tuple):
            move = self.game.moves.get(player = self.user)
            data = {
                "type":"winner_message",
                "user":str(self.user.get_decoded()["user"]),
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
                "scores":self.game.scores,
                "position":event.get("position"),
                "winning_moves":event.get("winning_moves")
            }
        ))

    def update_board(self, event):
        self.game.set_current_player()
        next_player =self.game.current_player.get_decoded()["user"]

        self.send(json.dumps(
            {
                "type":"update_board_message",
                "current_player":event.get("current_player"),
                "position":event.get("position"),
                "next_player":str(next_player),
                "player_mark":event.get("player_mark"),
                "count":self.game.move_count
            }
        ))

    def initialize_current_player(self, event):
        self.send(
            json.dumps(event)
        )

    def reload_page(self, event):
        self.send(
            json.dumps(event)
        )




    def disconnect(self, code):
        return super().disconnect(code)


class TicTacToeBOTConsumer(WebsocketConsumer):

    def connect(self):
        self.user = Session.objects.get(session_key = self.scope["session"].session_key)

        #self.user = self.scope["user"]
        self.game_uuid = str(self.scope["url_route"]["kwargs"]["uuid"])
        self.game = Game.objects.get(game_uuid = self.game_uuid)
        self.game.set_current_player()
        self.bot_player = Session.objects.get(session_key=settings.BOT_KEY)
    
        self.accept()


    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        text_data = json.loads(text_data)

        if text_data["type"] == "play_again":
            self.game.clear_game_data()
            self.send(
                json.dumps({
                    "type":"reload_page"
                })
            )
            return
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
          
        self.game.check_draw()
        
        self.send(json.dumps(
            {
                "type":"bot_update_board_message",
                "player_position":player_position,
                "bot_position":bot_move,
                "player_mark":player_mark,
                "bot_mark":bot_mark,
                "count":self.game.move_count
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
        
        if not is_winner and self.game.move_count >= 9:
            self.send(json.dumps(

                {
                "type":"draw_message",
            }
            ))
            return

        self.game.set_current_player()
        
        
    
    def disconnect(self, code):
        return super().disconnect(code)