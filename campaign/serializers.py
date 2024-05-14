from rest_framework import serializers
from campaign.models import FbCampaign


class FbCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = FbCampaign
        fields = '__all__'


class FbCampaignWithAdsBrief(FbCampaignSerializer):
    total_spent = serializers.SerializerMethodField()
    total_impressions = serializers.SerializerMethodField()
    total_ads_number = serializers.SerializerMethodField()

    def get_total_spent(self, obj):
        return obj.total_spent

    def get_total_impressions(self, obj):
        return obj.total_impressions

    def get_total_ads_number(self, obj):
        return obj.total_ads_number
