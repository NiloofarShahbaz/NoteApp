from django.db.models import Q

from rest_framework import generics
from rest_framework import permissions

from .serializers import *


class NoteListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(Q(owner=self.request.user) | Q(collaborators__in=[self.request.user, ]),
                                   is_archive=False, trash_delete_time=None)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NoteRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(is_archive=False, trash_delete_time=None, owner=self.request.user,
                                   pk=self.kwargs.get('pk'))
