from django.urls import path, re_path

from .views import (
    CreateProjectView,
    ProjectByLongIdContentView,
    ProjectByLongIdView,
    ProjectByShortIdContentView,
    ProjectByShortIdView,
    ShareProjectByLongIdView,
    ShareProjectByShortIdView,
)

urlpatterns = [
    re_path(
        r"^pxt/(?P<longid>\d{5}-\d{5}-\d{5}-\d{5})$",
        ProjectByLongIdView.as_view(),
        name="project-get-longid",
    ),
    re_path(
        r"^pxt/(?P<longid>\d{5}-\d{5}-\d{5}-\d{5})/text$",
        ProjectByLongIdContentView.as_view(),
        name="project-get-longid-content",
    ),
    re_path(
        r"^pxt/(?P<shortid>_\w{12})$",
        ProjectByShortIdView.as_view(),
        name="project-get-shortid",
    ),
    re_path(
        r"^pxt/(?P<shortid>_\w{12})/text$",
        ProjectByShortIdContentView.as_view(),
        name="project-get-shortid-content",
    ),
    path(
        "pxt/scripts",
        CreateProjectView.as_view(),
        name="project-create",
    ),
    re_path(
        r"^share/(?P<longid>\d{5}-\d{5}-\d{5}-\d{5})$",
        ShareProjectByLongIdView.as_view(),
        name="project-share-longid",
    ),
    re_path(
        r"^share/(?P<shortid>_\w{12})$",
        ShareProjectByShortIdView.as_view(),
        name="project-share-shortid",
    ),
]
