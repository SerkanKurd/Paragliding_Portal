from typing import Any

from django.conf import settings
from django.db import models
from django.utils.formats import date_format


class Pilot(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)  # noqa: DJ001
    profile_url = models.URLField(max_length=255, null=True, blank=True)  # noqa: DJ001
    level = models.CharField(  # noqa: DJ001
        max_length=2,
        choices=(("P2", "P2"), ("P3", "P3"), ("P4", "P4"), ("P5", "P5")),
        blank=True,
        null=True,
    )
    manager = models.ManyToManyField(settings.AUTH_USER_MODEL)
    is_updated = models.BooleanField(default=False)

    def __str__(self):
        return f"Pilot: {self.id} - {self.name}"  # type: ignore


class FlightData(models.Model):
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)
    flight_date = models.DateTimeField(blank=True, null=True)
    flight_date_str = models.CharField(max_length=50, blank=True, null=True)  # noqa: DJ001
    takeoff_time = models.DateTimeField(blank=True, null=True)
    takeoff_name = models.CharField(max_length=50, blank=True, null=True)  # noqa: DJ001
    landing_time = models.DateTimeField(blank=True, null=True)
    landing_name = models.CharField(max_length=50, blank=True, null=True)  # noqa: DJ001
    country = models.CharField(max_length=50, blank=True, null=True)  # noqa: DJ001
    flight_type = models.CharField(max_length=50, blank=True, null=True)  # noqa: DJ001
    paraglider = models.CharField(max_length=50, blank=True, null=True)  # noqa: DJ001
    duration = models.DurationField(blank=True, null=True)
    distance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    distance_olc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    points_olc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    points_olc_type = models.CharField(max_length=50, blank=True, null=True)  # noqa: DJ001
    distance_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    distance_from_takeoff = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    vario_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vario_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    altitude_takeoff = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    altitude_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    altitute_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    altitute_gain = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    speed_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    speed_avarage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # noqa: DJ001
    flight_url = models.URLField(max_length=255, unique=True, null=True, blank=True)
    file_name = models.CharField(max_length=200, blank=True, null=True)  # noqa: DJ001
    file_content = models.BinaryField(null=True, blank=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.flight_date:
            self.flight_date_str = date_format(self.flight_date)

    def __str__(self):
        return f"{self.pilot} - {self.flight_date_str} - {self.takeoff_name}"


class Wing(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    url = models.URLField(max_length=255, null=True, blank=True)  # noqa: DJ001
    manifacture = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    wing_class = models.CharField(max_length=10, blank=True, null=True)  # noqa: DJ001
    test = models.CharField(max_length=50, blank=True, null=True)  # noqa: DJ001
    safety = models.CharField(max_length=50, blank=True, null=True)  # noqa: DJ001
    weight_max = models.IntegerField(blank=True, null=True)
    weight_min = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Harness(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    manufacture = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    harness_type = models.CharField(max_length=50, blank=True, null=True)  # noqa: DJ001
    size = models.CharField(max_length=10, blank=True, null=True)  # noqa: DJ001
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.manufacture} {self.name}"


class Reserve(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    manufacture = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    reserve_type = models.CharField(max_length=50, blank=True, null=True)  # noqa: DJ001
    size = models.CharField(max_length=10, blank=True, null=True)  # noqa: DJ001
    weight_max = models.IntegerField(blank=True, null=True)
    weight_min = models.IntegerField(blank=True, null=True)
    manufacture_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.manufacture} {self.name}"
