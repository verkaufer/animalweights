from datetime import datetime
import pytz

from django.test import TransactionTestCase
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from animals.models import Animal, Weight


class WeightAPITests(TransactionTestCase):

    def setUp(self):
        self.client = APIClient()

        self.animal = Animal.objects.create(name="Ronald")

        if settings.USE_TZ:
            self.timezone = pytz.UTC
        else:
            self.timezone = None

    def test_no_weights_for_animal(self):
        """Assert endpoint returns null value when no weights exist for Animal"""
        requested_date = timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')

        resp = self.client.get(
            reverse('animals:estimated_weight', kwargs={'pk': self.animal.id}), 
            {'date':requested_date}
        )
        self.assertIsNone(resp.json()['estimated_weight'])

    def test_invalid_date_for_estimated_weight(self):
        """Assert error response returned when datetime param in url uses an invalid format"""
        # Swap Y and m in request datestring
        requested_date = timezone.now().strftime('%m-%Y-%dT%H:%M:%SZ')

        resp = self.client.get(
            reverse('animals:estimated_weight', kwargs={'pk': self.animal.id}), 
            {'date':requested_date}
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_estimated_weight_for_animal(self):
        """ 
        Assert endpoint returns correct result when trying to estimate weight based on 
        a date that does not exist in the database.
        """
        for i in range(1, 5):
            weight = float(500) + float(i*2)
            date_recorded = datetime(2018, 6, i*2, tzinfo=self.timezone)

            # This loop creates these example (Weight, DateRecorded):
            # (502, (2018, 06, 02))
            # (504, (2018, 06, 04))
            # (506, (2018, 06, 08))
            # (508, (2018, 06, 10))

            Weight.objects.create(
                animal=self.animal,
                recorded_weight=weight,
                recorded_at=date_recorded
            )

        # Assert a record for 2018-06-07 does NOT exist
        est_weight = Weight.objects.filter(recorded_at=datetime(2018, 6, 7))
        self.assertFalse(est_weight.exists())

        # Make request for estimated weight
        resp = self.client.get(
            reverse('animals:estimated_weight', kwargs={'pk': self.animal.id}),
            {'date': datetime(2018, 6, 7).strftime('%Y-%m-%dT%H:%M:%SZ')}
        )

        # Assert estimated weight is expected value
        self.assertEqual(resp.json()['estimated_weight'], float(507.0))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Assert estimated weight now stored in DB
        stored_estimated_weight = Weight.objects.filter(recorded_at=datetime(2018, 6, 7), estimated=True)
        self.assertTrue(stored_estimated_weight.exists())

    def test_estimated_weight_retrieved_from_db(self):
        # TODO: Use mock.patch to assert that the endpoint does DB lookup for recorded estimated weight
        # to see if it exists before running calculation.

        # Apply mock.patch to the interpolate function and assert it is NOT called
        pass
