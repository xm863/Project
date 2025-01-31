from django.contrib import admin
from django.urls import path
from apps.views import IndexView, AboutView, ContactView, MenuView, NewsView, NewsDetailView, UserCreateView, UserSigninView, UserLogoutView
from root import settings
from django.conf.urls.static import static
from apps.views import contactview

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
    path('logout/', UserLogoutView.as_view(), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)