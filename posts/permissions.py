from rest_framework import permissions

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

class PostPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user and request.user.is_authenticated
        else:
            return True
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.user == request.user
