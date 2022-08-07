from django.urls import path
from .consumers import TicTacToeConsumer,TicTacToeBOTConsumer


websocket_urlpatterns = [
    path("games/<uuid:uuid>/", TicTacToeConsumer.as_asgi(),),
    path("bot/games/<uuid:uuid>/", TicTacToeBOTConsumer.as_asgi(),)

]