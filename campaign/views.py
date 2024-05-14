from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import FbCampaign
from .serializers import FbCampaignSerializer
from rest_framework.exceptions import ValidationError


class CampaignPagination(PageNumberPagination):
    """
    Set default in case no page size is sent
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class FbCampaignListView(generics.ListAPIView):
    """
    A view for listing Facebook campaigns. It supports optional ordering based on
    query parameters in addition to pagination.

    Example:
        To retrieve a list of Facebook campaigns ordered by 'start_date', make a GET request to:
        /campaigns/?ordering=start_date
        /campaigns/?ordering=start_date&page=2&page_size=2
    """
    queryset = FbCampaign.objects.all()
    serializer_class = FbCampaignSerializer
    pagination_class = CampaignPagination

    def _validate_ordering(self, ordering: str) -> bool:
        """
        Validate that the provided ordering attribute is a valid field
        for ordering in the FbCampaign model

        :param ordering: The ordering attribute to validate.

        :return: True if the ordering attribute is valid; False otherwise.
        """
        # List of valid fields for ordering
        valid_fields = [field.name for field in FbCampaign._meta.get_fields()]
        # If the ordering attribute contains a hyphen for descending sorting, remove it
        if '-' in ordering:
            ordering = ordering.replace('-', '')
        return ordering in valid_fields

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            is_valid = self._validate_ordering(ordering)
            if is_valid:
                queryset = queryset.order_by(ordering)
            else:
                raise ValidationError({'error': 'Invalid ordering attribute.'})

        return queryset
