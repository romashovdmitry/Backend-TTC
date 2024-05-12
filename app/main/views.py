# DRF imports
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http.response import HttpResponse


# FIXME: добавть комментарий
@api_view(http_method_names=['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return HttpResponse(status=200)