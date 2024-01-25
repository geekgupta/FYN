# your_app_name/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import PricingConfig, Ride
from decimal import Decimal
from datetime import timedelta

class RideModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')

        self.pricing_config = PricingConfig.objects.create(
            base_price=50.0,
            additional_price=20.0,
            time_multiplier_factor=1.5,
            waiting_charge=5.0,
            distance_limit=10.0,
            day_of_week='Mon',
            is_active=True,
            created_by=self.user
        )

    def test_total_price_calculation(self):
        ride = Ride.objects.create(
            distance_traveled=Decimal('5.0'), 
            ride_time=timedelta(minutes=30),
            wait_time=timedelta(minutes=15),
            pricing_config=self.pricing_config
        )

        base_price = Decimal(self.pricing_config.base_price)
        additional_price = Decimal(self.pricing_config.additional_price)
        time_multiplier_factor = Decimal(self.pricing_config.time_multiplier_factor)
        waiting_charge = Decimal(self.pricing_config.waiting_charge)
        ride_time_seconds = Decimal(ride.ride_time.total_seconds())
        wait_time_seconds = Decimal(ride.wait_time.total_seconds())

        expected_total_price = (
            (base_price + (ride.distance_traveled * additional_price)) +
            (ride_time_seconds * time_multiplier_factor) +
            ((wait_time_seconds - 180) / 180 * waiting_charge)
        )

        saved_ride = Ride.objects.get(id=ride.id)

        self.assertEqual(saved_ride.total_price, expected_total_price)
