from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from paragliding.models import Pilot, FlightData, Wing, Harness, Reserve

User = get_user_model()

class ParaglidingModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testpilot", password="password123")
        
        self.pilot = Pilot.objects.create(
            name="Serkan Kurd",
            level="P4",
            is_updated=True
        )
        self.pilot.manager.add(self.user)

        self.wing = Wing.objects.create(
            name="Chili 5",
            manifacture="Skywalk",
            wing_class="EN-B",
            weight_min=85,
            weight_max=105
        )

        self.harness = Harness.objects.create(
            name="Range X-Alps",
            manufacture="Skywalk",
            harness_type="Pod",
            size="M",
            weight=1.8
        )

        self.reserve = Reserve.objects.create(
            name="Pepper Cross Light",
            manufacture="Skywalk",
            reserve_type="Square",
            size="100",
            weight_max=100,
            weight_min=0,
            manufacture_date=timezone.now().date()
        )

    def test_pilot_str(self):
        self.assertEqual(str(self.pilot), f"Pilot: {self.pilot.id} - Serkan Kurd")

    def test_wing_str(self):
        self.assertEqual(str(self.wing), "Chili 5")

    def test_harness_str(self):
        self.assertEqual(str(self.harness), "Skywalk Range X-Alps")

    def test_reserve_str(self):
        self.assertEqual(str(self.reserve), "Skywalk Pepper Cross Light")

    def test_flight_data_creation_and_str(self):
        flight = FlightData.objects.create(
            pilot=self.pilot,
            flight_date=timezone.now(),
            takeoff_name="Babadag",
            landing_name="Oludeniz",
            duration=timezone.timedelta(hours=1, minutes=30),
            distance=45.2
        )
        self.assertIn("Serkan Kurd", str(flight))
        self.assertIn("Babadag", str(flight))
