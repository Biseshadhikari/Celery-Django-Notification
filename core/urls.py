from django.urls import path
from . import views
urlpatterns = [
    path("index/",views.index),
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/update/', views.post_update, name='post_update'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('managenotification/',views.manageNotification,name = "manageNotification")
]