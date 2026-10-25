import json

from django.core.files.base import ContentFile
from rest_framework import serializers

from ..models import PythonProject, Submission


class PythonProjectSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="ulid")
    source = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = PythonProject
        fields = (
            "id",
            "name",
            "description",
            "created",
            "meta",
            "source",
        )

    @staticmethod
    def get_source(obj):
        if not obj.content.name:
            return None

        with obj.content.open("r") as file:
            return json.load(file).get("source")


class PythonProjectCreateSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=26)
    name = serializers.CharField(max_length=50, allow_blank=True)
    description = serializers.CharField(max_length=200, allow_blank=True)
    meta = serializers.JSONField()
    source = serializers.CharField()

    @staticmethod
    def validate_meta(value):
        if len(json.dumps(value)) > 100 * 1024:
            raise serializers.ValidationError("Must not be larger than 100 KiB.")

        return value

    @staticmethod
    def validate_source(value):
        if len(value) > 1024 * 1024:
            raise serializers.ValidationError("Must not be larger than 1 MiB.")

        return value

    def create(self, validated_data):
        project = PythonProject(
            name=validated_data.get("name"),
            description=validated_data.get("description"),
            meta=validated_data.get("meta", {}),
        )

        content = json.dumps({"source": validated_data.get("source")}).encode("utf-8")
        project.content.save("content.json", ContentFile(content), save=False)

        project.save()
        return project


class PythonProjectSubmitSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(queryset=PythonProject.objects.all(), slug_field="ulid")

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
