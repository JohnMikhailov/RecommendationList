from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, user):
        return (request.method in permissions.SAFE_METHODS) or (user == request.user)


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return view.kwargs['pk'].isdigit() and request.user.id == int(view.kwargs['pk'])

    def has_object_permission(self, request, view, obj):
        return obj == request.user
