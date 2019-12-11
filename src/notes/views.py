from django.core.exceptions import MultipleObjectsReturned

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import *


class NoteListCreateView(generics.ListCreateAPIView):
    """
    model : Note
    -List
    -Create input: title(optional)
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(setting__user=self.request.user, setting__is_archived=False,
                                   setting__trash_delete_time=None)


class NoteRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    model : Note
    -Retrieve
    -Update input: title
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(setting__user=self.request.user, setting__is_archived=False,
                                   setting__trash_delete_time=None, pk=self.kwargs.get('pk'))


class ContentCreateView(generics.CreateAPIView):
    """
    model : Content
    -Create input: text, status(H,T,F)(optional)
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ContentSerializer


class ContentUpdateView(generics.UpdateAPIView):
    """
    model: Content
    -Update input: text, status(H,T,F)
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ContentSerializer
    lookup_url_kwarg = 'content_pk'

    def get_queryset(self):
        return Content.objects.filter(note=self.kwargs["pk"], note__setting__user=self.request.user,
                                      note__setting__trash_delete_time=None, pk=self.kwargs['content_pk'])


class SettingUpdateView(generics.UpdateAPIView):
    """
    model: Note Setting
    -Update input: is_archived, is_pinned, order, color
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SettingSerializer

    def get_queryset(self):
        return Setting.objects.filter(note=self.kwargs["pk"], user=self.request.user,
                                      note__setting__trash_delete_time=None)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, note=self.kwargs["pk"], user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class LabelListView(generics.ListAPIView):
    """
    model: Label
    -List
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LabelSerializer

    def get_queryset(self):
        return Label.objects.filter(setting__user=self.request.user)


class LabelCreateView(generics.CreateAPIView):
    """
    model: Label
    -Create input: text
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LabelSerializer


class LabelUpdateView(generics.UpdateAPIView):
    """
    model: Label
    -Update input: text
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LabelSerializer
    lookup_url_kwarg = 'label_pk'

    def get_queryset(self):
        return Label.objects.filter(setting__user=self.request.user, setting__note=self.kwargs['pk'],
                                    pk=self.kwargs['label_pk'], setting__trash_delete_time=None)


class SettingLabelCreate(generics.CreateAPIView):
    """
    Adds a specific label to user's note of choice
    -Create
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SettingLabelSerializer
