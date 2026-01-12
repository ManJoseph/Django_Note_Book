from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.note_list),
    path('create-user/', views.create_user),
    path('users/', views.users)
]