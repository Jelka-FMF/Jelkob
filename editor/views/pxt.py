import json

from django.conf import settings
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response

from ..models import PXTProject, Submission
from ..serializers import PXTProjectCreateSerializer, PXTProjectSerializer, ProjectSubmitSerializer


class PXTProjectMixin(generics.RetrieveAPIView):
    queryset = PXTProject.objects.all()
    serializer_class = PXTProjectSerializer


class PXTProjectByLongIdView(PXTProjectMixin):
    lookup_field = "longid"


class PXTProjectByShortIdView(PXTProjectMixin):
    lookup_field = "shortid"


class PXTProjectContentMixin(generics.GenericAPIView):
    queryset = PXTProject.objects.all()

    def get(self, request, *args, **kwargs):
        project = self.get_object()
        content = {}

        if project.content.name:
            with project.content.open("r") as file:
                content = json.load(file)

        return Response(content)


class PXTProjectContentByLongIdView(PXTProjectContentMixin):
    lookup_field = "longid"


class PXTProjectContentByShortIdView(PXTProjectContentMixin):
    lookup_field = "shortid"


@method_decorator(csrf_exempt, name="dispatch")
class PXTCreateProjectView(generics.CreateAPIView):
    queryset = PXTProject.objects.all()
    serializer_class = PXTProjectCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        model = serializer.save()
        data = PXTProjectSerializer(model).data

        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


@method_decorator(csrf_exempt, name="dispatch")
class PXTSubmitProjectView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = ProjectSubmitSerializer


class PXTShareProjectMixin(generics.GenericAPIView):
    queryset = PXTProject.objects.all()

    def get(self, request, *args, **kwargs):
        project = self.get_object()
        return redirect(f"{settings.JELKLY_EDITOR_URL}#{settings.JELKLY_EDITOR_ACTION}:{project.longid}")


class PXTShareProjectByLongIdView(PXTShareProjectMixin):
    lookup_field = "longid"


class PXTShareProjectByShortIdView(PXTShareProjectMixin):
    lookup_field = "shortid"
