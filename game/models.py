from tokenize import group
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from uuid import uuid4

from django.forms import ValidationError
# Create your models here.

User = get_user_model()

wining_moves = [["1", "4", "7"],["2","5","8"],["3","6","9"],
["1", "2", "3"],["4","5","6"],["7","8","9"],
["1", "5", "9"],["3","5","9"]]

class Game(models.Model):
    
    STATUS = [
        ("in_progess", "in_progress"),
        ("finished", "finished")
    ]
    game_uuid = models.UUIDField(default=uuid4(), editable=False)
    players = models.ManyToManyField(User)
    status = models.CharField(choices=STATUS, max_length=20)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", null=True, blank=True)
    current_player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="current_player")


    def get_invite_link(self):
        pass
    
    @property
    def player_1(self):
        return self.players.first()
    
    @property
    def player_2(self):
        if self.players.all().count() == 2:
            return self.players.last()
        return None

    def set_current_player(self):
        if self.current_player:
            self.current_player = self.players.exclude(id = self.current_player.id).first()
        else:
            self.current_player = self.player_1
            self.save()
          

    def add_new_player(self, player):
        if self.players.all().count() < 2:
            self.players.add(player)
        else:
            raise Exception("A Game cannot have more than two players")

    def check_winner(self):
        current_move = self.moves.get(player=self.current_player).positions
        for wining_move in wining_moves:
            print(wining_move, current_move, set(wining_move) & set(current_move))
            if set(wining_move) & set(current_move) == set(wining_move):
                self.winner = self.current_player
                self.status = "finished"
                self.save()
                return True
        return False


 #   def save(self, *args, **kwargs) -> None:
 #       check  = self.players.all().count() > 2
 #       print(check)
 #       if check:
 #           raise ValidationError("The length of player cannot be more than two")
 #       return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Game {self.game_uuid}"

class Move(models.Model):
    PLAYER_MARK = [
        ("x", "X"),
        ("O", "O")
    ]
    uuid = models.UUIDField(default=uuid4(), editable=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="moves")
    positions = ArrayField(models.CharField(max_length=5))
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    player_mark = models.CharField(choices=PLAYER_MARK, max_length=3, default="X")

    def __str__(self):
        return f"{self.player_mark}-{self.positions}"

    def assign_player_mark(self):
        pass







