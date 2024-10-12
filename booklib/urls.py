from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from booklib import settings
# library/urls.py
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Booklib API",
      default_version='v1',
      description="Test API for Booklib",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



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
    
urlpatterns += [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
