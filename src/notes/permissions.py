from rest_framework import permissions

from .models import *


class HasNote(permissions.BasePermission):
    def has_permission(self, request, view):
        setting = Setting.objects.filter(user_id=request.user.id, note_id=view.kwargs['pk']).exists()
        return setting


class HasLabel(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        setting_label = SettingLabel.objects.filter(setting__user_id=request.user.id, label_id=obj).exists()
        return setting_label
