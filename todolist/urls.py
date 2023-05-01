from django.contrib import admin
from django.urls import path, include

from todolist import settings

urlpatterns = [
    path('core/', include(('core.urls', 'core'))),
    path('admin/', admin.site.urls),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("goals/", include(("goals.urls", 'goals'))),
    path("bot/", include(("bot.urls", 'bot'))),
]

if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls'))
    ]
