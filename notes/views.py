from django.http import JsonResponse
from notes.serializers import UserSerializer, NoteSerializer
from notes.models import User, Note
from rest_framework.decorators import api_view

# Create your views here.
@api_view(["GET"])
def note_list(request):
    notes = Note.objects.all()
    serializer = NoteSerializer(notes, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(["POST"])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return JsonResponse(serializer.data)

@api_view(["GET"])
def users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data,  safe=False)