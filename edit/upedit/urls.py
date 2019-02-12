from django.urls import path, include, re_path
from . import views
urlpatterns = [
    path('', views.index),
    path('upload/', views.upload, name='upload'),
    path('edit/<int:key>/', views.edit),
    #path('edit/<int:key>/bl/', views.bl, name='bl'),
    re_path(r'^edit/(?P<key>[0-9]*)/bl', views.bl, name='bl'),
    path('edit/<int:key>/rt/', views.rotatation, name='rt'),
    path('edit/<int:key>/rs/', views.rotatation, name='rs'),
    path('edit/<int:key>/cr/', views.croper, name='cr'),
]
