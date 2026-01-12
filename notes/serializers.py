from rest_framework import serializers
from .models import Note, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        re_password = serializers.CharField(required=True, write_only=True)
        model = User
        fields = (
            'first_name',
            'username',
            'email',
            'password',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True, 'write_only': True},
        }

    def validate(self, value):
        if value['re_password'] != value['password']:
            raise serializers.ValidationError({'password': "Passwords do not match"})
        return super().validate(value)

        if value['email'] and User.objects.filter(email=value['email']).exists():
            raise serializers.ValidationError({'email': "Email already exists"})
        return super().validate(value)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            username=self.validated_data['username'],
            password=self.validated_data['password']
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

class TokenObtainPairSerializer(serializers.Serializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Added custom claims
        token['username'] = user.username
        token['email'] = user.email
        return token