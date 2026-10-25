from django.urls import re_path

from ..views import ShareProject

urlpatterns = [
    re_path(
        r"^share/(?P<ulid>\w{26})$",
        ShareProject.as_view(),
        name="project-share",
    ),
]
