from rest_framework import permissions


class CanCreateCourse(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ["owner", "admin", "seller"]
        )
