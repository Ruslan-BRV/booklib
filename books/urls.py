from django.urls import include, path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'genre', views.GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path("", views.BooksView.as_view(), name='catalog'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='detail_book_by_id'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)