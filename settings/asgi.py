import os
from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter
# from channels.auth import AuthMiddlewareStack
# import content.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     # "websocket": AuthMiddlewareStack(
#     #     URLRouter(
#     #         content.routing.websocket_urlpatterns
#     #     )
#     # ),
# })


application = get_asgi_application()