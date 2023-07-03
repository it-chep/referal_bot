from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_v1/', include('telegrambot.api_urls')),
    path('', include('telegrambot.urls'))
]

urlpatterns += [
    re_path(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
