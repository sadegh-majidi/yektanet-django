from rest_framework.permissions import BasePermission


class IsAdvertiser(BasePermission):
    def has_permission(self, request, view):
        try:
            return bool(not request.user.advertiser.is_deleted)
        except:
            return False
