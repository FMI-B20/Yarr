from rest_framework.pagination import LimitOffsetPagination, Response
from rest_framework import permissions

class Pagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(data)

class IsStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return request.user.is_staff == True
