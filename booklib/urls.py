from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from booklib import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("books.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                      # другие URL-паттерны
                  ] + urlpatterns
