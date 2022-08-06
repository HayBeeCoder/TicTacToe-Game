from django.dispatch import Signal, receiver
from .models import Game, Move
from django.db.models.signals import post_save

create_move = Signal(["player", "game"])


@receiver(create_move)
def create_move_receiver(sender, player, game, *args, **kwargs):
    Move.objects.create(game=game, player=player, positions=[])


@receiver(post_save, sender = Game)
def create_move_on_save(sender, instance, created, *args, **kwargs):
    if created:
        pass
            #Move.objects.create(game=instance, player=instance.player_1, positions=[])




