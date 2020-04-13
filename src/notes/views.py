from rest_framework import generics

from .serializers import *
from .permissions import *


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
    permission : HasNote
    -Retrieve
    -Update input: title
    """
    permission_classes = (permissions.IsAuthenticated, HasNote)
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(setting__user=self.request.user, setting__is_archived=False,
                                   setting__trash_delete_time=None, pk=self.kwargs.get('pk'))


class ContentCreateView(generics.CreateAPIView):
    """
    model : Content
    permission : HasNote
    -Create input: text, status(H,T,F)(optional)
    """
    permission_classes = (permissions.IsAuthenticated, HasNote)
    serializer_class = ContentSerializer


class ContentUpdateView(generics.UpdateAPIView):
    """
    model: Content
    permission : HasNote
    -Update input: text, status(H,T,F)
    """
    permission_classes = (permissions.IsAuthenticated, HasNote)
    serializer_class = ContentSerializer
    lookup_url_kwarg = 'content_pk'

    def get_queryset(self):
        return Content.objects.filter(note=self.kwargs["pk"], note__setting__user=self.request.user,
                                      note__setting__trash_delete_time=None, pk=self.kwargs['content_pk'])


class SettingUpdateView(generics.UpdateAPIView):
    """
    model: Setting
    permission : HasNote
    -Update input: is_archived, is_pinned, order, color
    """
    permission_classes = (permissions.IsAuthenticated, HasNote)
    serializer_class = SettingSerializer

    def get_queryset(self):
        return Setting.objects.filter(note=self.kwargs["pk"], user=self.request.user,
                                      note__setting__trash_delete_time=None)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, note=self.kwargs["pk"], user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class SettingAddCollaborator(generics.CreateAPIView):
    """
    model: Setting
    permission : HasNote
    Adds a collaborator to note
    -Create input: user_email
    """
    permission_classes = (permissions.IsAuthenticated, HasNote)
    serializer_class = SettingCreateOnlySerializer


class LabelListView(generics.ListAPIView):
    """
    url: /api/labels/
    model: Label
    -List
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = LabelSerializer

    def get_queryset(self):
        return Label.objects.filter(setting__user=self.request.user).distinct()


class LabelCreateView(generics.CreateAPIView):
    """
    url: /api/notes/<int:pk>/labels/
    model: Label
    permission: HasNote
    -Create input: text
    """
    permission_classes = (permissions.IsAuthenticated, HasNote)
    serializer_class = LabelSerializer


class LabelUpdateView(generics.UpdateAPIView):
    """
    url: /api/notes/<int:pk>/label/<int:label_pk>/
    model: Label
    permission: HasNote, HasLabel
    -Update input: text
    """
    permission_classes = (permissions.IsAuthenticated, HasNote, HasLabel)
    serializer_class = LabelSerializer
    lookup_url_kwarg = 'label_pk'

    def get_queryset(self):
        return Label.objects.filter(setting__user=self.request.user, setting__note=self.kwargs['pk'],
                                    pk=self.kwargs['label_pk'], setting__trash_delete_time=None)


class SettingLabelCreate(generics.CreateAPIView):
    """
    Adds a specific label to user's note of choice
    url : /api/notes/<int:pk>/labels/<int:label_pk>/add/
    permission : HasNote, HasLabel
    -Create
    """
    permission_classes = (permissions.IsAuthenticated, HasNote, HasLabel)
    serializer_class = SettingLabelSerializer
