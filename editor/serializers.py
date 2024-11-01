import calendar
import json

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="longid")
    persistId = serializers.CharField(source="longid")
    time = serializers.SerializerMethodField()
    kind = serializers.SerializerMethodField()
    thumb = serializers.SerializerMethodField()

    class Meta:
        model = Project

        fields = (
            "id",
            "shortid",
            "persistId",
            "name",
            "description",
            "time",
            "kind",
            "target",
            "editor",
            "meta",
            "thumb",
        )

    @staticmethod
    def get_time(obj):
        return calendar.timegm(obj.created.utctimetuple()) if obj.created else None

    @staticmethod
    def get_kind(obj):
        return "script"

    @staticmethod
    def get_thumb(obj):
        return False


class ProjectCreateSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=True)
    description = serializers.CharField(max_length=255, allow_blank=True)
    target = serializers.CharField(max_length=50)
    targetVersion = serializers.CharField(max_length=50)
    editor = serializers.CharField(max_length=50)
    header = serializers.CharField()
    text = serializers.CharField()
    meta = serializers.JSONField()

    @staticmethod
    def validate_target(value):
        if value != "jelka":
            raise serializers.ValidationError("Must be a valid target.")
        return value

    @staticmethod
    def validate_header(value):
        try:
            json.loads(value)
        except json.JSONDecodeError as error:
            raise serializers.ValidationError("Must be a valid JSON content.") from error
        return value

    @staticmethod
    def validate_text(value):
        try:
            json.loads(value)
        except json.JSONDecodeError as error:
            raise serializers.ValidationError("Must be a valid JSON content.") from error
        return value

    def create(self, validated):
        project = Project(
            name=validated.get("name"),
            description=validated.get("description"),
            target=validated.get("target"),
            editor=validated.get("editor"),
            meta=validated.get("meta", {}),
        )

        content = ContentFile(validated.get("text").encode("utf-8"))
        project.content.save("content.json", content)

        project.save()
        return project
