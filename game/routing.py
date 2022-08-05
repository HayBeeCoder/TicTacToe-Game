from django.urls import path
from .consumers import TicTacToeConsumer


websocket_urlpatterns = [
    path("games/<uuid:uuid>/", TicTacToeConsumer.as_asgi(),)
]