from django.contrib import admin
from django.urls import path, include
import chat_app.ws_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_app.urls')),
    path('api/chat/', include('chat_app.urls')),
]

ws_urlpatterns = [
]



ws_urlpatterns += chat_app.ws_urls.urlpatterns