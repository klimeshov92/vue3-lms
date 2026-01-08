"""
ASGI config for light project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'light.settings')

# ✅ 1. СНАЧАЛА инициализируем Django
django_asgi_app = get_asgi_application()

# ✅ 2. ТОЛЬКО ПОСЛЕ этого импортируем всё, что тянет модели
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chats.routing import websocket_urlpatterns
from chats.middlewares import JWTAuthMiddleware

# ✅ 3. ОДИН application
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
