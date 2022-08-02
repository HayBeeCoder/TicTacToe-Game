from channels
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TicTacToe.settings')

asgi_application = get_asgi_application()
