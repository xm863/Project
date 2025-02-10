from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from root import settings
from apps.views import (
    IndexView, AboutView, ContactView, MenuView, NewsView, 
    NewsDetailView, UserCreateView, UserSigninView, UserLogoutView, 
    contactview, comment_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('contact/', contactview, name="contact"),
    path('about/', AboutView.as_view(), name="about"),
    path('menu/', MenuView.as_view(), name="menu"),
    path('news/', NewsView.as_view(), name="news"),
    path('news/<int:pk>/', NewsDetailView.as_view(), name="news-detail"),
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', UserSigninView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('comment/<int:news_id>/', comment_view, name='comment_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
