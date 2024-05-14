from .serializers import CampaignMetricsSerializer, FbCampaignWithAdsBrief
from django.db.models import Sum
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FbCampaign
from ad.models import Ad
from ad.serializers import AdSerializer, AdMetricsSerializer
from utils.mixins import OrderingMixin
from utils.pagination import CustomPagination
from rest_framework.exceptions import NotFound
from django.core.exceptions import FieldError, ValidationError


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
        try:
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
        except FbCampaign.DoesNotExist:
            raise NotFound


class CampaignMetricsAPIView(APIView):
    """
    Retrieve campaign metric within a specified date range.


    :param start_date (str): Start date of the date range in 'YYYY-MM-DD' format.
    :param end_date (str): End date of the date range in 'YYYY-MM-DD' format.
    :param metric (str): The metric to aggregate for ads associated with campaigns.

    :returns: A JSON response containing campaign IDs and aggregated metric values.

    Example:
        GET /campaign-metrics/?start_date=2024-01-01&end_date=2024-01-31&metric=clicks
    """

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        metric = request.query_params.get('metric')

        if not all([start_date, end_date, metric]):
            return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ads = Ad.objects.filter(
                fb_campaign__start_date__gte=start_date, fb_campaign__end_date__lte=end_date)
            ads = ads.values('fb_campaign_id').annotate(metric_sum=Sum(metric))
        except FieldError:
            return Response({'error': 'Invalid metric field'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CampaignMetricsSerializer(ads, many=True)
        return Response(serializer.data)


class CampaignADMetricsAPIView(APIView):
    """
    Retrieve campaign metric within a specified date range.


    :param start_date (str): Start date of the date range in 'YYYY-MM-DD' format.
    :param end_date (str): End date of the date range in 'YYYY-MM-DD' format.
    :param metric (str): The metric to aggregate for ads associated with campaigns.

    :returns: A JSON response containing campaign IDs and aggregated metric values.

    Example:
        GET /campaigns/1/metrics/?metric=clicks
    """

    def get(self, request, id):
        metric = request.query_params.get('metric', '')

        # Validate if the metric is a valid field of the Ad model
        if not hasattr(Ad, metric):
            return Response({'error': 'Invalid metric'}, status=400)

        # Retrieve ads for the given fb_campaign_id with only the specified metric
        ads = Ad.objects.filter(fb_campaign_id=id)

        serializer = AdMetricsSerializer(
            ads, many=True, context={'metric': metric})

        return Response(serializer.data)
