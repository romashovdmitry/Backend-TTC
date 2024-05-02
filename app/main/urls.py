# Django imports
from django.contrib import admin
from django.urls import path, include, re_path

# DRF imports
from rest_framework.permissions import AllowAny

# JWT imports
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from main.views import health_check

schema_view = get_schema_view(
    openapi.Info(
        title="Table Tennis Club Backend API", default_version="v1", description="API endpoints described here", terms_of_service=""
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    re_path(
        r"^api-docs/swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    re_path(r"^api-docs/swagger$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^api-docs/redoc$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    path("admin/", admin.site.urls),
    path('api/v1/user/', include("user.urls")),
    path('/', health_check)
]

