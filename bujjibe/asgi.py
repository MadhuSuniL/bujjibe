import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from bujjibe.urls import ws_urlpatterns
from auth_app.ws_auth_middleware import WsAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bujjibe.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            WsAuthMiddleware(
                URLRouter(ws_urlpatterns)
            )
        ),
    }
)