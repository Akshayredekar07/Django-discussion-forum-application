from django.contrib import admin
from django.urls import path, include
from main import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('detail/<slug:slug>/', views.detail, name='detail'),  
    path('posts/<slug:slug>/', views.posts, name='posts'),  
    path('create_post', views.create_post, name='create_post'),  


    # URLs from installed apps
    path('tinymce/', include('tinymce.urls')),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),


    path('account/', include('register.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)