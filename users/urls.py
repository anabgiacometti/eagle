from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.list, name='user-list'),
    path('list', views.list, name='user-list'),
    path('detail/', views.detail, name='user-detail'),
    path('detail/<id>', views.detail, name='user-detail'),
    path('deactivate/<id>', views.deactivate, name='user-deactivate'),
    path('activate/<id>', views.activate, name='user-activate'),
    path('delete/<id>', views.delete, name='user-delete'),
]