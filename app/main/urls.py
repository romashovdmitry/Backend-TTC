# Django imports
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

# Swagger imports
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

# import config, constants data
from main.settings import MEDIA_ROOT, MEDIA_URL

# import views, custom foos, classes
from main.views import health_check


urlpatterns = [
    # for docker health-checker
    path('/', health_check),
    # Swagger urls
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    # admin url
    path("asdnjkasdnj1/123/qsadm6k6/easd/admin/", admin.site.urls),
    # projects urls
    path('api/v1/user/', include("user.urls")),
    path('api/v1/club/', include("club.urls")),
    path('api/v1/tournament/', include("tournament.urls")),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
