
from .views import FbCampaignListView
from django.urls import path

urlpatterns = [
    path('', FbCampaignListView.as_view(), name='fb-campaign-list'),

]
