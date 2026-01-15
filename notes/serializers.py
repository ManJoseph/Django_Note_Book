import datetime
from rest_framework import serializers
from .models import Note, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'username',
            'email',
            'password',
            're_password',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True, 'write_only': True},
            're_password': {'write_only': True},
        }

    def validate(self, data):
        if data.get('re_password') != data.get('password'):
            raise serializers.ValidationError({'password': "Passwords do not match"})
        if data.get('email') and User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': "Email already exists"})
        return data

    def create(self, validated_data):
        validated_data.pop('re_password', None)
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    
    def create_super_user(self, Validate_data):
        Validate_data.pop('re_password', None)
        user = user.objects.create_superuser(
            first_name=validated_data['first_name'],
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = (
            'id',
            'user',
            'title',
            'content',
            'created_at',
            'updated_at',
        )

        def create(self, validated_data):
            note = Note.objects.create_note(
                title=validated_data['title'],
                content=validated_data['content']
            )
            return note

        def update(self, instance, validated_data):
            instance.title = validated_data.get('title', instance.title)
            instance.content = validated_data.get('content', instance.content)
            instance.save()
            return instance

        def delete(self, instance):
            instance.delete_note()
            return instance

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        # Allow login via email
        email = attrs.get('email')
        password = attrs.get('password')
        
        if not (email):
            raise serializers.ValidationError("Email required.")
        
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid email or password.")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email/username or password.")
        
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive.")
        
        refresh = self.get_token(user)
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
            }
        }
        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['first_name'] = user.first_name
        token['username'] = user.username
        token['email'] = user.email
        return token

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(required=True, write_only=True)