import json

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Project, Submission
from .serializers import ProjectCreateSerializer, ProjectSerializer, ProjectSubmitSerializer


class ProjectByLongIdView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = "longid"


class ProjectByLongIdContentView(generics.GenericAPIView):
    @staticmethod
    def get(request, longid):
        project = get_object_or_404(Project, longid=longid)
        content = {}
        if project.content.name:
            with project.content.open("r") as file:
                content = json.load(file)
        return Response(content)


class ProjectByShortIdView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = "shortid"


class ProjectByShortIdContentView(generics.GenericAPIView):
    @staticmethod
    def get(request, shortid):
        project = get_object_or_404(Project, shortid=shortid)
        content = {}
        if project.content.name:
            with project.content.open("r") as file:
                content = json.load(file)
        return Response(content)


class CreateProjectView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        model = serializer.save()
        data = ProjectSerializer(model).data

        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class SubmitProjectView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = ProjectSubmitSerializer


class ShareProjectByLongIdView(View):
    @staticmethod
    def get(request, longid):
        project = get_object_or_404(Project, longid=longid)
        return redirect(f"{settings.EDITOR_URL}#{settings.EDITOR_ACTION}:{project.longid}")


class ShareProjectByShortIdView(View):
    @staticmethod
    def get(request, shortid):
        project = get_object_or_404(Project, shortid=shortid)
        return redirect(f"{settings.EDITOR_URL}#{settings.EDITOR_ACTION}:{project.longid}")
