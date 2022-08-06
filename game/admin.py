from django.contrib import admin
from .models import Game, Move
from typing import Any
#Register your models here.

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):

    def save_related(self, request: Any, form: Any, formsets: Any, change: Any) -> None:
        super().save_related(request, form, formsets, change)
        Move.objects.create(game=form.instance, player=form.instance.player_1, positions=[])



admin.site.register(Move)
