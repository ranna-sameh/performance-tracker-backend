from django.db import models
from campaign.models import FbCampaign


class Ad(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    fb_campaign = models.ForeignKey(FbCampaign, on_delete=models.CASCADE)
    age = models.CharField(max_length=10)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    interest = models.IntegerField()
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    spent = models.FloatField()
    total_conversion = models.IntegerField()
    approved_conversion = models.IntegerField()
