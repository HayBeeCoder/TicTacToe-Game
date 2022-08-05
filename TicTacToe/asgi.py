import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TicTacToe.settings')

asgi_application = get_asgi_application()


import game.routing

application = ProtocolTypeRouter({
  "http": asgi_application,
  "websocket": 
  AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                game.routing.websocket_urlpatterns
            )     
    ),
)})
