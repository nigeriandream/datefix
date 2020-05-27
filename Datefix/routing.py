from django.conf.urls import url
from django.urls import path, include
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter
from Chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter([
        
            path('chat/', ChatConsumer),
            # path('chat/<int:thread_id>', ChatConsumer)
        
    ])))
})