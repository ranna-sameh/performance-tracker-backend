from django.db import models
from django.db.models import Sum, Count


class FbCampaign(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    xyz_campaign_id = models.IntegerField()

    @property
    def total_impressions(self):
        # Aggregate total impressions from ads related to this campaign
        return self.ad_set.aggregate(total_impressions=Sum('impressions'))['total_impressions'] or 0

    @property
    def total_spent(self):
        # Aggregate total spent from ads related to this campaign
        return self.ad_set.aggregate(total_spent=Sum('spent'))['total_spent'] or 0

    @property
    def total_ads_number(self):
        # Count the total number of ads related to this campaign
        return self.ad_set.count()