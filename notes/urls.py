from django.urls import path, include
from notes.views import UserViewSet, LoginAPIView, NotesAPIView
from rest_framework import routers

router=routers.DefaultRouter()
router.register('users',UserViewSet, basename="user")
router.register('notes',NotesAPIView, basename="notes")
router.register('login',LoginAPIView, basename="login")

urlpatterns = [
    path('',include(router.urls))
]