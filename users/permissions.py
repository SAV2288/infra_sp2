from rest_framework import permissions


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):

        return request.user.is_authenticated and request.user.is_superuser


class IsAccountAdminOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):

        return request.user.is_staff or request.method in permissions.SAFE_METHODS


class RoleAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):

        return request.user.role == 'admin' or request.user.is_superuser


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user or request.user.role == 'admin' or \
               request.user.is_superuser or request.user.role == 'moderator'


class AuthorizedPermission(permissions.BasePermission):
    def has_permission(self, request, view):

        return request.user.is_authenticated or request.method in permissions.SAFE_METHODS
