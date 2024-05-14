from rest_framework import serializers
from campaign.models import FbCampaign


class FbCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = FbCampaign
        fields = '__all__'
