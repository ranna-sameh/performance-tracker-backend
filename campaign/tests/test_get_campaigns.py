from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from campaign.models import FbCampaign


class FbCampaignListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('fb-campaign-list')
        self.campaign1 = FbCampaign.objects.create(
            start_date='2024-01-01', end_date='2024-01-10', xyz_campaign_id=1)
        self.campaign2 = FbCampaign.objects.create(
            start_date='2024-02-01', end_date='2024-02-10', xyz_campaign_id=1)

    def test_list_campaigns(self):
        response = self.client.get(self.url)
        results = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 2)

    def test_positive_ordering_campaigns(self):
        response = self.client.get(self.url, {'ordering': 'start_date'})
        results = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(results[0]['id'], self.campaign1.id)
        self.assertEqual(results[1]['id'], self.campaign2.id)

    def test_negative_ordering_campaigns(self):
        response = self.client.get(self.url, {'ordering': '-start_date'})
        results = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(results[0]['id'], self.campaign2.id)
        self.assertEqual(results[1]['id'], self.campaign1.id)

    def test_pagination(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)

        response = self.client.get(self.url, {'page_size': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_invalid_ordering_param(self):
        response = self.client.get(self.url, {'ordering': 'invalid_field'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
