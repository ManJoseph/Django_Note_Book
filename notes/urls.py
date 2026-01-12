from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.note_list),
    path('create-user/', views.create_user),
    path('users/', views.users),
    path('create-superuser/', views.create_superuser),
    path('login/', views.login_user)
]