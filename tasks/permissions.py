from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    # not applied when creating objects
    def has_object_permission(self, request, view, obj):
        return obj.job.board.user == request.user
