from rest_framework import permissions


class IsOwnerOfAddress(permissions.BasePermission):
    """
    Custom permission to only allow users to delete their own addresses.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the address
        return obj.user_profile.user == request.user
