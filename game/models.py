from statistics import mode
from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from uuid import uuid4

from django.forms import ValidationError
from django.contrib.sessions.models import Session
# Create your models here.

User = get_user_model()

wining_moves = [["1", "4", "7"],["2","5","8"],["3","6","9"],
["1", "2", "3"],["4","5","6"],["7","8","9"],
["1", "5", "9"],["3","5","7"]]

class Game(models.Model):

    IN_PROGRESS, FINISHED = range(2)
    VERSUS, BOT = range(2)

    
    STATUS = [
        (IN_PROGRESS, "In_Progress"),
        (FINISHED, "Finished")
    ]
    TYPE = [
        (VERSUS, "Versus"),
        (BOT, "Bot")
    ]
    versus_type = models.CharField(max_length=10, choices=TYPE, default="Versus")
    created_by = models.ForeignKey(Session, on_delete=models.SET_NULL, related_name="created_by", null=True, blank=True)
    game_uuid = models.UUIDField(default=uuid4(), editable=False)
    players = models.ManyToManyField(Session)
    status = models.CharField(choices=STATUS, max_length=20, default="In_Progress")
    winner = models.ForeignKey(Session, on_delete=models.SET_NULL, related_name="winner", null=True, blank=True)
    current_player = models.ForeignKey(Session
    , on_delete=models.SET_NULL, related_name="current_player", null=True, blank=True)


    def get_absolute_url(self):
        return reverse("game_view", kwargs = {"uuid":self.game_uuid})
    
    @property
    def player_1(self):
        return self.created_by
    
    @property
    def player_2(self):
        if self.players.all().count() == 2:
            return self.players.exclude(session_key = self.created_by.session_key).first()
        return None

    def set_current_player(self):
        if self.current_player:
            self.current_player = self.players.exclude(session_key = self.current_player.session_key).first()
        else:
            self.current_player = self.player_1
        self.save()
          

    def add_new_player(self, player, mark="O"):
        if self.players.all().count() < 2:
            self.players.add(player)
            Move.objects.create(game=self, player=player, positions=[], player_mark = mark)

        else:
            raise Exception("A Game cannot have more than two players")

    def check_winner(self):
        current_move = self.moves.get(player=self.current_player).positions
        for wining_move in wining_moves:
            moves = set(wining_move) & set(current_move)
            if moves == set(wining_move):
                self.winner = self.current_player
                self.status = "Finished"
                self.save()
                return True, moves
        return False


 #   def save(self, *args, **kwargs) -> None:
 #       check  = self.players.all().count() > 2
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
    positions = ArrayField(models.CharField(max_length=5, blank=True, null=True), blank=True, null=True)
    player = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)
    player_mark = models.CharField(choices=PLAYER_MARK, max_length=3, default="X")

    def __str__(self):
        return f"{self.player_mark}-{self.positions}"

    def assign_player_mark(self):
        pass







