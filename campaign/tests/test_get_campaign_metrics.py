from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from campaign.models import FbCampaign
from ad.models import Ad


class CampaignMetricsAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('campaign_metrics')

        self.fb_campaign = FbCampaign.objects.create(
            start_date='2024-01-01',
            end_date='2024-01-31',
            xyz_campaign_id=1
        )
        Ad.objects.create(
            fb_campaign=self.fb_campaign,
            age='25-34',
            gender='M',
            interest=1,
            impressions=1000,
            clicks=50,
            spent=10.0,
            total_conversion=5,
            approved_conversion=3
        )

    def test_valid_request(self):
        response = self.client.get(
            f"{self.url}?start_date=2024-01-01&end_date=2024-01-31&metric=clicks")
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {'fb_campaign_id': self.fb_campaign.id, 'metric_sum': 50}
        ]
        self.assertEqual(result, expected_data)

    def test_missing_parameters(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_date_format(self):
        response = self.client.get(
            f"{self.url}?start_date=2024/01/01&end_date=2024-01-31&metric=clicks")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_metric_field(self):
        response = self.client.get(
            f"{self.url}?start_date=2024-01-01&end_date=2024-01-31&metric=invalid_metric")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_campaigns_found(self):
        response = self.client.get(
            f"{self.url}?start_date=2025-01-01&end_date=2025-01-31&metric=clicks")
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Empty results
        self.assertFalse(result)
