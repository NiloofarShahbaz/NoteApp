from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    collaborators = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    labels = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Note
        exclude = ['trash_delete_time', ]

    def save(self, **kwargs):
        kwargs["owner"] = self.context['request'].user
        super().save(**kwargs)
