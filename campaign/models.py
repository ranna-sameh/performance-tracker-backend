from django.db import models


class FbCampaign(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    xyz_campaign_id = models.IntegerField()
