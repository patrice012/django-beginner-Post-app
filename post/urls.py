from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name= 'index'),
    path('search/', views.search, name='search'),
    path('blog/', views.post_list, name =  'post-list'),
    path('create/', views.post_create, name = 'post-create'),
    path('post/<int:id>/', views.post_detail, name = 'post-detail'),
    path('post/<int:id>/update/', views.post_update, name = 'post-update'),
    path('post/<int:id>/delete/', views.post_delete, name ='post-delete'),
]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
