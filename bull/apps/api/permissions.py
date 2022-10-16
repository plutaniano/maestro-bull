from rest_framework import permissions


class IsAdminOrSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or int(view.kwargs["pk"]) == request.user.pk
