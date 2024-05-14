
from .views import FbCampaignListView, FbCampaignDetailView
from django.urls import path

urlpatterns = [
    path('', FbCampaignListView.as_view(), name='fb-campaign-list'),
    path('<int:id>', FbCampaignDetailView.as_view(),
         name='fb-campaign-details'),

]
