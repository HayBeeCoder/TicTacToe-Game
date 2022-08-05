from django.shortcuts import render
from .models import Game, Move
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

def game_view(request, uuid):

    game = Game.objects.get(game_uuid=uuid)
    moves = game.moves.all()
    player_1 = game.player_1
    player_2 = game.player_2
    players = game.players.all()
    print(player_1,player_2,moves)
    context={
        "game":game,
        "moves":moves,
        "player_1":player_1,
        "player_2":player_2,
        "range": [str(i) for i in range(1,10)],
        "player_1_moves":moves.get(player=player_1),
        "player_2_moves":moves.get(player=player_2)
        
    }
    return render(request, "index.html", context=context)