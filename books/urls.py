from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path("", views.BooksView.as_view(), name='catalog'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='detail_book_by_id'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)