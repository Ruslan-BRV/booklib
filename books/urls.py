from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'genre', views.GenreViewSet)

urlpatterns = [
    path('books/copies/', views.BookViewSet.as_view({'get': 'list_top_books'}), name='top-books'),
    path('authors/<int:pk>/stat/', views.AuthorViewSet.as_view({'get': 'stat'}), name='author-stat'),
    path('authors/stat/', views.AuthorViewSet.as_view({'get': 'stats'}), name='authors-stat'),
    path('books/delivery/', views.BookDeliveryView.as_view(), name='book-delivery'),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
