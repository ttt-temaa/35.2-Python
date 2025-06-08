from rest_framework import permissions


class IsModer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, object):
        if object.owner == request.user:
            return True
        return False
