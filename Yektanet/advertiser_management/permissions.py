from rest_framework.permissions import BasePermission
from .models import Advertiser


class IsAdvertiser(BasePermission):
    def has_permission(self, request, view):
        return Advertiser.objects.filter(username=request.user.username).exists()
