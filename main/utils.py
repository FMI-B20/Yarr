from rest_framework.pagination import PageNumberPagination, Response

class Pagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(data)
