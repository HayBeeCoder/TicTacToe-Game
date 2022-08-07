from distutils.log import INFO
import random
import re
from uuid import uuid4
from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, Move
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# Create your views here.

User = get_user_model()

def game_view(request, uuid):

    game = Game.objects.get(game_uuid=uuid)
    moves = game.moves.all()
    player_1 = game.player_1
    player_2 = game.player_2
    players = game.players.all()
    context={
        "game":game,
        "moves":moves,
        "player_1":player_1,
        "player_2":player_2,
        "range": [str(i) for i in range(1,10)],
        "player_1_moves":moves.get(player=player_1),
        "player_2_moves":moves.get(player=player_2) if len(moves) > 1 else ""
        
    }
    print(game.versus_type == "BOT")
    return render(request, "game.html", context=context)

@csrf_exempt
def index(request:HttpRequest):
    #request.session["user"] = f"player_{random.randint(0,100)}"
    #print(request.session.keys(), request.session.values())
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("invite-link"):
            uuid = request.POST.get("invite-link")
            game = get_object_or_404(Game, game_uuid=uuid)
            return redirect(game)  
        elif request.POST.get("new-game-vs"):
            
            new_game = Game.objects.create(game_uuid =uuid4() ,
                                        status = "In_Progress",
                                         created_by=request.user,
                                         versus_type="Versus")
            new_game.add_new_player(player=request.user, mark="X")
            
            new_game.save()
            messages.add_message(request, level=INFO, message=f"Invite Link: {str(new_game.game_uuid)}")
            return redirect(new_game)
        elif request.POST.get("new-game-bot"):
            BOT = User.objects.get(username = "BOT")

            new_game = Game.objects.create(game_uuid =uuid4() ,
                                        status = "In_Progress",
                                         created_by=request.user,
                                         versus_type="BOT")
            new_game.add_new_player(player=request.user, mark="X")
            new_game.add_new_player(player=BOT, mark="O")

            
            new_game.save()
            return redirect(new_game)  

            #)
    print(request.POST)         

    return render(request,"index.html")