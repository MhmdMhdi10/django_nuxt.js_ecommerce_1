from rest_framework.permissions import BasePermission


class HasOTPCode(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj is not None:
            return True
        else:
            return False
