from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from campaign.models import FbCampaign
from ad.models import Ad


class AdDetailViewTest(TestCase):
    def setUp(self):
        self.fb_campaign = FbCampaign.objects.create(
            start_date='2024-01-01', end_date='2024-01-10', xyz_campaign_id=1)
        self.ad1 = Ad.objects.create(fb_campaign=self.fb_campaign, age="18-24", gender="M", interest=1,
                                     impressions=1000, clicks=50, spent=10.5, total_conversion=5, approved_conversion=3)

    def _get_url(self, ad_id):
        # Constructing the URL with the ad_id and ordering as query parameters
        return reverse('ad-details', kwargs={'pk': ad_id})

    def test_ad_detail(self):
        url = self._get_url(self.ad1.id)
        response = self.client.get(url)
        results = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(results['id'], self.ad1.id)
        self.assertEqual(results['fb_campaign'], self.ad1.fb_campaign.id)
        self.assertEqual(results['age'], self.ad1.age)
        self.assertEqual(results['gender'], self.ad1.gender)
        self.assertEqual(results['interest'], self.ad1.interest)
        self.assertEqual(results['impressions'], self.ad1.impressions)
        self.assertEqual(results['clicks'], self.ad1.clicks)
        self.assertEqual(results['spent'], self.ad1.spent)
        self.assertEqual(
            results['total_conversion'], self.ad1.total_conversion)
        self.assertEqual(
            results['approved_conversion'], self.ad1.approved_conversion)

    def test_ad_detail_id_not_found(self):
        url = self._get_url(12345)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
