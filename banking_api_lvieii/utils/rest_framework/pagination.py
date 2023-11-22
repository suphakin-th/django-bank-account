from django.conf import settings
from django.core.paginator import InvalidPage
from rest_framework import pagination
from rest_framework.exceptions import NotFound
from rest_framework.response import Response  # Do not change!!


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        page_size = self.get_page_size(self.request)
        return Response({
            'next': self.page.next_page_number() if self.page.has_next() else None,
            'next_url': self.get_next_link(),
            'previous': self.page.previous_page_number() if self.page.has_previous() else None,
            'previous_url': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': page_size if page_size is not None else self.page_size,
            'results': data
        })

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                return pagination._positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass
        page_size = getattr(request, 'page_size', None)
        return page_size
