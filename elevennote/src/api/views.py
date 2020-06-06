from rest_framework import viewsets

from notes.models import Note
from accounts.models import User
from .serializers import NoteSerializer, UserSerializer

from django.http import JsonResponse
from rest_framework import viewsets, status
from django.core import serializers


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    # def filter_queryset(self, queryset):
    #     queryset = Note.objects.filter(owner=self.request.user)
    #     return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        serializer.save()


def filter_note(request, name):
    if request.method == "GET":
        notes = Note.objects.filter(
            tags__contains=name
        )

        notes |= Note.objects.filter(
            title__contains=name
        )

        return JsonResponse(serializers.serialize('json', list(notes)), safe=False,)
