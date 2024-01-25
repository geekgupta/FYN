from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class PricingConfig(models.Model):
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    additional_price = models.DecimalField(max_digits=8, decimal_places=2)
    time_multiplier_factor = models.FloatField()
    waiting_charge = models.DecimalField(max_digits=5, decimal_places=2)
    distance_limit = models.DecimalField(max_digits=5, decimal_places=2)
    day_of_week = models.CharField(max_length=10, choices=[
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ])
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Ride(models.Model):
    distance_traveled = models.DecimalField(max_digits=5, decimal_places=2)
    ride_time = models.DurationField()
    wait_time = models.DurationField()
    pricing_config = models.ForeignKey(PricingConfig, on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.pricing_config:
            base_price = Decimal(self.pricing_config.base_price)
            additional_price = Decimal(self.pricing_config.additional_price)
            time_multiplier_factor = Decimal(self.pricing_config.time_multiplier_factor)
            waiting_charge = Decimal(self.pricing_config.waiting_charge)
            ride_time_seconds = Decimal(self.ride_time.total_seconds())
            wait_time_seconds = Decimal(self.wait_time.total_seconds())
            total_price = (
                (base_price + (self.distance_traveled * additional_price)) +
                (ride_time_seconds * time_multiplier_factor) +
                ((wait_time_seconds - 180) / 180 * waiting_charge)
            )

            self.total_price = total_price

        super().save(*args, **kwargs)