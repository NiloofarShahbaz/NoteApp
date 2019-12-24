from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from .models import *


class LabelSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        note_pk = self.context['view'].kwargs['pk']
        setting = get_object_or_404(Setting, note=note_pk, user=self.context['request'].user, trash_delete_time=None)
        label = Label.objects.create(**validated_data)
        SettingLabel.objects.create(label=label, setting=setting)
        return label

    class Meta:
        model = Label
        fields = ('id', 'text',)


class SettingSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True, read_only=True)
    is_owner = serializers.BooleanField(read_only=True)

    class Meta:
        model = Setting
        exclude = ('user', 'trash_delete_time', 'note')


class SettingCreateOnlySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', queryset=get_user_model().objects.all())

    def create(self, validated_data):
        note_pk = self.context['view'].kwargs['pk']
        user = get_object_or_404(get_user_model(), pk=validated_data['user'].pk)
        setting = Setting.objects.create(user_id=user.id, note_id=note_pk)
        return setting

    class Meta:
        model = Setting
        fields = ('user', )


class SettingLabelSerializer(serializers.ModelSerializer):
    label = LabelSerializer(read_only=True)
    setting = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        note_pk = self.context['view'].kwargs['pk']
        label_pk = self.context['view'].kwargs['label_pk']
        user = self.context['request'].user
        setting = get_object_or_404(Setting, note=note_pk, user=user, trash_delete_time=None)
        setting_label = SettingLabel.objects.create(label_id=label_pk, setting=setting)
        return setting_label

    def validate(self, attrs):
        user = self.context['request'].user
        note_pk = self.context['view'].kwargs['pk']
        label_pk = self.context['view'].kwargs['label_pk']

        setting_label = SettingLabel.objects.filter(setting__note_id=note_pk, label_id=label_pk, setting__user_id=user,
                                                    setting__trash_delete_time=None)

        if setting_label:
            raise ValidationError(_('The fields {label, setting} must make a unique set.'), code='unique')
        return attrs

    class Meta:
        model = SettingLabel
        fields = ('id', 'label', 'setting')


class ContentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        note = get_object_or_404(Note, pk=self.context['view'].kwargs['pk'], setting__trash_delete_time=None,
                                 setting__user=self.context['request'].user)

        return Content.objects.create(note=note, **validated_data)

    class Meta:
        model = Content
        fields = ('pk', 'order', 'status', 'text')


class NoteSerializer(serializers.ModelSerializer):
    content_set = ContentSerializer(many=True, read_only=True)
    setting_set = serializers.SerializerMethodField()

    def get_setting_set(self, obj):
        setting_set = Setting.objects.filter(user=self.context['request'].user, note=obj)
        serializer = SettingSerializer(setting_set, many=True)
        return serializer.data

    def create(self, validated_data):
        note = Note.objects.create(**validated_data)
        # create a note setting for this user(which is the owner)
        Setting.objects.create(note=note, user=self.context['request'].user, is_owner=True)
        return note

    class Meta:
        model = Note
        fields = ('id', 'title', 'content_set', 'users', 'setting_set')
