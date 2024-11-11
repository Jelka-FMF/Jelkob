import calendar
import json

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Project, Submission


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
    name = serializers.CharField(max_length=50, allow_blank=True)
    description = serializers.CharField(max_length=200, allow_blank=True)
    target = serializers.CharField(max_length=50)
    targetVersion = serializers.CharField(max_length=50)
    editor = serializers.CharField(max_length=50)
    header = serializers.CharField()
    text = serializers.CharField()
    meta = serializers.JSONField()

    @staticmethod
    def validate_target(value: str):
        if value != "jelka":
            raise serializers.ValidationError("Must be a valid target.")

        return value

    @staticmethod
    def validate_header(value: str):
        if len(value) > 100 * 1024:
            raise serializers.ValidationError("Must not be larger than 100 KiB.")

        try:
            json.loads(value)
        except json.JSONDecodeError as error:
            raise serializers.ValidationError("Must be a valid JSON content.") from error

        return value

    @staticmethod
    def validate_text(value: str):
        if len(value) > 1024 * 1024:
            raise serializers.ValidationError("Must not be larger than 1 MiB.")

        try:
            json.loads(value)
        except json.JSONDecodeError as error:
            raise serializers.ValidationError("Must be a valid JSON content.") from error

        return value

    @staticmethod
    def validate_meta(value: dict):
        if len(json.dumps(value)) > 100 * 1024:
            raise serializers.ValidationError("Must not be larger than 100 KiB.")

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


class ProjectSubmitSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field="shortid")

    class Meta:
        model = Submission

        fields = (
            "name",
            "description",
            "duration",
            "author",
            "school",
            "project",
        )
