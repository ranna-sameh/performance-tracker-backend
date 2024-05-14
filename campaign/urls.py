
from .views import FbCampaignListView, FbCampaignDetailView, CampaignMetricsAPIView, CampaignADMetricsAPIView
from django.urls import path

urlpatterns = [
    path('', FbCampaignListView.as_view(), name='fb-campaign-list'),
    path('<int:id>', FbCampaignDetailView.as_view(),
         name='fb-campaign-details'),
    path('metrics/', CampaignMetricsAPIView.as_view(),
         name='campaign_metrics'),
    path('<int:id>/metrics/', CampaignADMetricsAPIView.as_view(),
         name='campaign_ads_metrics'),
]
