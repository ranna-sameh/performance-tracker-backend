from django.test import TestCase
from django.db import models
from django.urls import reverse
from utils.mixins import OrderingMixin, validate_ordering
from campaign.models import FbCampaign
from rest_framework.exceptions import ValidationError
from unittest.mock import MagicMock


class OrderingMixinTestCase(TestCase):
    def setUp(self):
        # Define a sample model
        class SampleModel(models.Model):
            name = models.CharField(max_length=100)
            age = models.IntegerField()

        self.model = SampleModel

    def test_validate_ordering(self):
        # Test valid ordering attribute
        valid_fields = ['name', 'age']
        for field in valid_fields:
            self.assertTrue(validate_ordering(self.model, field))

        # Test invalid ordering attribute
        invalid_fields = ['invalid_field', 'age__invalid']
        for field in invalid_fields:
            self.assertFalse(validate_ordering(self.model, field))

    def test_get_ordered_queryset(self):
        # Create a mock request object with query_params
        request = MagicMock()
        request.query_params = {'ordering': 'name'}

        # Create a mock queryset
        queryset = MagicMock()

        # Apply the ordering using the mixin
        ordered_queryset = OrderingMixin.get_ordered_queryset(
            request, queryset, self.model)

        # Assert that the queryset's order_by method was called with the correct parameter
        queryset.order_by.assert_called_once_with('name')

    def test_get_ordered_queryset_invalid_ordering(self):
        # Create a mock request object with invalid ordering attribute
        request = MagicMock()
        request.query_params = {'ordering': 'invalid_field'}

        queryset = MagicMock()

        # Test that ValidationError is raised for invalid ordering attribute
        with self.assertRaises(ValidationError):
            ordered_queryset = OrderingMixin.get_ordered_queryset(
                request, queryset, self.model)
