"""
URL configuration for Jelkob project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
import django.views.i18n

urlpatterns = [
    path("accounts/login/", LoginView.as_view(template_name="frontend/login.html"), name="login"),
    path("accounts/logout/", LogoutView.as_view(template_name="frontend/logout.html"), name="logout"),
    path("i18n/setlang/", django.views.i18n.set_language, name="set-language"),
    path("admin/", admin.site.urls),
    path("runner/", include("runner.urls")),
    path("editor/", include("editor.urls")),
    path("", include("frontend.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
