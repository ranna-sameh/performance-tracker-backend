from django.test import TestCase
from django.urls import reverse
from campaign.models import FbCampaign
from ad.models import Ad
from rest_framework import status


class FbCampaignDetailViewTest(TestCase):
    def setUp(self):

        self.fb_campaign = FbCampaign.objects.create(
            start_date="2022-01-01", end_date="2022-01-31", xyz_campaign_id=123)
        self.ad1 = Ad.objects.create(fb_campaign=self.fb_campaign, age="18-24", gender="M", interest=1,
                                     impressions=1000, clicks=50, spent=10.5, total_conversion=5, approved_conversion=3)
        self.ad2 = Ad.objects.create(fb_campaign=self.fb_campaign, age="25-34", gender="F", interest=2,
                                     impressions=2000, clicks=30, spent=15.75, total_conversion=8, approved_conversion=6)

    def _get_url(self, campaign_id, ordering=""):
        # Constructing the URL with the campaign_id and ordering as query parameters
        url = reverse('fb-campaign-details', kwargs={'id': campaign_id})
        if ordering:
            url += f"?ordering={ordering}"
        return url

    def test_get_campaign_detail(self):
        url = self._get_url(self.fb_campaign.id)
        response = self.client.get(url)
        results = response.data['results']
        campaign_results = results['campaign']

        self.assertEqual(response.status_code, 200)
        self.assertIn('campaign', results)
        self.assertIn('ads', results)
        self.assertEqual(campaign_results['start_date'], "2022-01-01")
        self.assertEqual(campaign_results['end_date'], "2022-01-31")
        self.assertEqual(campaign_results['xyz_campaign_id'], 123)
        self.assertEqual(len(results['ads']), 2)

    def test_get_campaign_detail_with_ordering(self):
        url = self._get_url(self.fb_campaign.id, ordering='-clicks')
        response = self.client.get(url)
        results = response.data['results']
        ads_results = results['ads']

        self.assertEqual(response.status_code, 200)
        self.assertIn('campaign', results)
        self.assertIn('ads', results)
        self.assertEqual(len(ads_results), 2)
        # Check if the ads are ordered by clicks in descending order
        self.assertEqual(ads_results[0]['clicks'], 50)
        self.assertEqual(ads_results[1]['clicks'], 30)

    def test_get_campaign_detail_not_found(self):
        url = self._get_url(12345)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
