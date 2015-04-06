from rest_framework.pagination import LimitOffsetPagination, Response

class Pagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(data)
