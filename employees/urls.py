from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.list, name='employee-list'),
    path('detail/', views.detail, name='employee-detail'),
    path('detail/<id>', views.detail, name='employee-detail'),
    # path('deactivate/<id>', views.deactivate, name='user-deactivate'),
    # path('activate/<id>', views.activate, name='user-activate'),
    path('delete/<id>', views.delete, name='employee-delete'),
]