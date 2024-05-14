from rest_framework import generics
from .serializers import AdSerializer
from ad.models import Ad
from ad.serializers import AdSerializer
from utils.mixins import OrderingMixin
from utils.pagination import CustomPagination


class AdListView(generics.ListAPIView):
    """
    A view for ads. It supports optional ordering based on
    query parameters in addition to pagination.

    Example:
        To retrieve a list of ads ordered by 'clicks', make a GET request to:
        /ads/?ordering=clicks
        /ads/?ordering=clicks&page=2&page_size=2
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply ordering to campaigns queryset
        queryset = OrderingMixin.get_ordered_queryset(
            self.request, queryset, Ad)

        return queryset
