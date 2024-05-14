from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ad.models import Ad
from campaign.models import FbCampaign


class CampaignADMetricsAPITest(TestCase):
    def setUp(self):
        # Create test data

        self.fb_campaign = FbCampaign.objects.create(
            start_date="2022-01-01", end_date="2022-01-31", xyz_campaign_id=123)
        self.fb_campaign_2 = FbCampaign.objects.create(
            start_date="2022-01-01", end_date="2022-01-31", xyz_campaign_id=123)
        self.ad1 = Ad.objects.create(fb_campaign_id=self.fb_campaign.id, age='30-34', gender='M', interest=1,
                                     impressions=1000, clicks=50, spent=10.0, total_conversion=5, approved_conversion=3)
        self.ad2 = Ad.objects.create(fb_campaign_id=self.fb_campaign.id, age='25-29', gender='F', interest=2,
                                     impressions=800, clicks=60, spent=12.0, total_conversion=6, approved_conversion=4)
        self.ad3 = Ad.objects.create(fb_campaign_id=self.fb_campaign_2.id, age='30-34', gender='M', interest=1,
                                     impressions=1200, clicks=70, spent=15.0, total_conversion=7, approved_conversion=5)

    def _get_url(self, campaign_id):
        # Constructing the URL with the campaign_id
        return reverse('campaign_ads_metrics', kwargs={'id': campaign_id})

    def test_valid_metric(self):
        url = self._get_url(self.fb_campaign.id)
        response = self.client.get(url, {'metric': 'clicks'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], self.ad1.id)
        self.assertEqual(response.data[1]['id'], self.ad2.id)
        self.assertTrue('clicks' in response.data[0])

    def test_invalid_metric(self):
        url = self._get_url(self.fb_campaign.id)
        response = self.client.get(url, {'metric': 'invalid_metric'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid metric'})

    def test_no_metric_provided(self):
        url = self._get_url(self.fb_campaign.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid metric'})
