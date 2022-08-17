from distutils.log import INFO
import random
import re
from uuid import uuid4
from django.shortcuts import render, get_object_or_404, redirect

from django.conf import settings
from .models import Game, Move
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# Create your views here.

User = get_user_model()


from django.contrib.sessions.models import Session

def game_view(request, uuid):

    game = Game.objects.get(game_uuid=uuid)
    moves = game.moves.all()
    player_1 = game.player_1
    player_2 = game.player_2
    players = game.players.all()
    context={
        "game":game,
        "moves":moves,
        "player_1":player_1.get_decoded()["user"],
        "player_2":player_2.get_decoded()["user"] if player_2 else player_2,
        "range": [str(i) for i in range(1,10)],
        "player_1_moves":moves.get(player=player_1),
        "player_2_moves":moves.get(player=player_2) if len(moves) > 1 else "",
        "player_1_scores":game.scores.get(str(player_1)),
        "player_2_scores":0 if not game.scores.get(str(player_2)) else game.scores.get(str(player_2))

        
    }
    return render(request, "game.html", context=context)

@csrf_exempt
def index(request:HttpRequest):
    request.session["user"] = f"player_{random.randint(0,100)}"
    if request.method == "POST":
        request.session["user"] = f"player_{random.randint(0,100)}"
        session_obj = Session.objects.get(session_key=request.session.session_key)


        if request.POST.get("invite-link"):
            uuid = request.POST.get("invite-link")
            game = get_object_or_404(Game, game_uuid=uuid)
            return redirect(game)  
        elif request.POST.get("new-game-vs"):
            
            new_game = Game.objects.create(game_uuid =uuid4() ,
                                        status = "In_Progress",
                                         created_by=session_obj,
                                         versus_type="Versus")
            new_game.add_new_player(player=session_obj, mark="X")
            
            new_game.save()
            messages.add_message(request, level=INFO, message=f"Invite Link: {str(new_game.game_uuid)}")
            return redirect(new_game)
        elif request.POST.get("new-game-bot"):
            BOT = Session.objects.get(session_key=settings.BOT_KEY)
            request.session["user"] = f"player_{random.randint(0,100)}"
            session_obj = Session.objects.get(session_key=request.session.session_key)
            new_game = Game.objects.create(game_uuid =uuid4() ,
                                        status = "In_Progress",
                                         created_by=session_obj,
                                         versus_type="BOT")
            new_game.add_new_player(player=session_obj, mark="X")
            new_game.add_new_player(player=BOT, mark="O")

            
            new_game.save()
            return redirect(new_game)  

            #)

    return render(request,"index.html")