from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('pets/', include('pets.urls', namespace='pets')),
    path('', include('accounts.urls', namespace='accounts')),
    # path('', include('telegram_bot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
