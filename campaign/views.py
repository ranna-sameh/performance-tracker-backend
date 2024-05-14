from rest_framework import generics
from rest_framework.views import APIView
from .models import FbCampaign
from .serializers import FbCampaignWithAdsBrief
from ad.models import Ad
from ad.serializers import AdSerializer
from utils.mixins import OrderingMixin
from utils.pagination import CustomPagination


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
    serializer_class = FbCampaignWithAdsBrief
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply ordering to campaigns queryset
        queryset = OrderingMixin.get_ordered_queryset(
            self.request, queryset, FbCampaign)

        return queryset


class FbCampaignDetailView(APIView):
    """
    A view for handling Facebook campaign by id.

    Example:
        To retrieve a Facebook campaign of id =1 and ads ordered by 'clicks', make a GET request to:
        /campaigns/1/?ordering=clicks
        /campaigns/1?ordering=clicks&page=2&page_size=2
    """

    def get(self, request, id):
        """
        Retrieve details of a Facebook campaign and associated ads. It supports optional ordering based on
        query parameters in addition to pagination.

        :param request: The request object.
        :param id: The ID of the Facebook campaign to retrieve.

        :return: Response containing details of the Facebook campaign and associated ads.
        """
        campaign = FbCampaign.objects.get(pk=id)
        ads = Ad.objects.filter(fb_campaign_id=id)

        # Apply ordering to ads queryset
        ads = OrderingMixin.get_ordered_queryset(request, ads, Ad)

        # Pagination on ads
        paginator = CustomPagination()
        paginated_ads = paginator.paginate_queryset(ads, request)

        campaign_serializer = FbCampaignWithAdsBrief(campaign)
        ad_serializer = AdSerializer(paginated_ads, many=True)
        return paginator.get_paginated_response({"campaign": campaign_serializer.data,
                                                 "ads":  ad_serializer.data})
