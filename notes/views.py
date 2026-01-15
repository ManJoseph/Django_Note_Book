
from notes.serializers import UserSerializer, NoteSerializer, LoginSerializer, CustomTokenObtainPairSerializer
from notes.models import User, Note
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from notes.serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import  viewsets
from rest_framework.permissions import AllowAny
from rest_framework import filters

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'username', 'first_name']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            self.get_serializer(user).data,
            status=status.HTTP_201_CREATED
        )
class LoginAPIView(viewsets.ViewSet):
    custom_serializer = CustomTokenObtainPairSerializer
    queryset = User.objects.all()
    permission_classes = ()
 
   
    def create(self, request, *args, **kwargs):
        '''
        User login with Jwt token
        params : username , password
        return : Jwt token
        '''
        serializer = self.custom_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class NotesAPIView(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'user__email', 'user__username']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        note = serializer.save()
        
        return Response(
            self.get_serializer(note).data,
            status=status.HTTP_201_CREATED
        )
